import ast
import copy

import pandas as pd  # Make sure you have pandas installed


from datetime import datetime


class Discount:
    def __init__(self, discount_id, discount_type=None, details=None, buy_quantity=0, get_quantity=0,
                 amount=0.0, strategy=None, strategy_limit=None,
                 lifetime=None, limit=None, discount_taxable=True):
        """
        Initialize a Discount instance.

        Args:
            discount_id (str): Unique identifier for the discount.
            discount_type (str): Type of the discount.
            details (str): Description or details of the discount.
            buy_quantity (int): Quantity required to qualify for the discount.
            get_quantity (int): Quantity given for free or at a discount.
            amount (float): Discount amount.
            strategy (str): Strategy for applying the discount.
            strategy_limit (int): Limit on the number of uses for the strategy.
            lifetime (str): Lifetime of the discount in MM/DD/YYYY format.
            limit (int): Total limit for the discount usage.
            discount_taxable (bool): Whether the discount is taxable.
        """
        self.discount_id = discount_id
        self.discount_type = discount_type
        self.details = details
        self.buy_quantity = buy_quantity
        self.get_quantity = get_quantity
        self.amount = amount
        self.strategy = strategy
        self.strategy_limit = strategy_limit
        self.limit = limit if limit is not None else float('inf')
        self.discount_taxable = discount_taxable
        self.buy_items = set()
        self.get_items = set()
        self.eligible_ids = set()
        self.applied_count = 0

        if lifetime:
            try:
                self.lifetime = datetime.strptime(lifetime, '%m/%d/%Y')
            except ValueError:
                raise ValueError("Lifetime date must be in the format MM/DD/YYYY")
        else:
            self.lifetime = None

    def __repr__(self):
        return f"Discount({self.discount_id}, {self.discount_type}, {self.amount}, {self.discount_taxable})"





    def apply_discount(self, cart):
        total_discount = 0.0

        # Check customer's current limit for this discount
        customer_limit_remaining = self.get_current_limit(cart.customer)

        if customer_limit_remaining <= 0:
            print(f"[INFO] Customer has reached the discount limit for {self.discount_id}. No discounts applied.")
            return total_discount

        remaining_limit = min(self.limit - self.applied_count, customer_limit_remaining)

        if remaining_limit <= 0:
            print(f"[INFO] Discount limit reached for {self.discount_id}. No further discounts applied.")
            return total_discount

        # Step 1: Apply external_discount
        if self.discount_type == 'external_discount':
            total_discount += self._apply_external_discount(cart, remaining_limit)


        # Step 2: Apply buy_get_free
        if self.discount_type == 'buy_get_free':
            total_discount += self._apply_buy_get_free(cart, remaining_limit)


        # Step 3: Apply bakers_dozen
        if self.discount_type == 'bakers_dozen':
            total_discount += self._apply_bakers_dozen(cart)


        else:
            print(f"[WARNING] Unrecognized discount type '{self.discount_type}' for discount ID {self.discount_id}")

        # Update the applied count globally
        self.applied_count += (self.limit - remaining_limit)

        return total_discount



    # def apply_discount(self, cart):
    #     total_discount = 0.0

    #     # Check customer's current limit for this discount
    #     customer_limit_remaining = self.get_current_limit(cart.customer)

    #     if customer_limit_remaining <= 0:
    #         print(f"[INFO] Customer has reached the discount limit for {self.discount_id}. No discounts applied.")
    #         return total_discount

    #     remaining_limit = min(self.limit - self.applied_count, customer_limit_remaining)

    #     if remaining_limit <= 0:
    #         print(f"[INFO] Discount limit reached for {self.discount_id}. No further discounts applied.")
    #         return total_discount

    #     if self.discount_type == 'external_discount':
    #         total_discount = self._apply_external_discount(cart, remaining_limit)

    #     if self.discount_type == 'buy_get_free':
    #         total_discount = self._apply_buy_get_free(cart, remaining_limit)

    #     if self.discount_type == 'bakers_dozen':
    #         total_discount = self._apply_bakers_dozen(cart.items.values())

    #     else:
    #         print(f"[WARNING] Unrecognized discount type '{self.discount_type}' for discount ID {self.discount_id}")

    #     # Update the applied count globally
    #     self.applied_count += (self.limit - remaining_limit)

    #     return total_discount

    # def apply_discount(self, cart):
    #     total_discount = 0.0

    #     if self.discount_type == 'external_discount':
    #         for item in cart.items.values():
    #             if self.is_item_eligible_for_discount(item):
    #                 discount_quantity = min(item.quantity - item.discounted_quantity, self.amount)
    #                 if discount_quantity > 0:
    #                     print(f"[DEBUG] Applying external discount: {self.amount} to {discount_quantity} items.")
    #                     item.mark_for_discount(discount_quantity, self.amount, self.discount_id)
    #                     total_discount += discount_quantity * self.amount

    #     elif self.discount_type == 'buy_get_free':
    #         total_discount = self._apply_buy_get_free(cart)

    #     elif self.discount_type == 'bakers_dozen':
    #         total_discount = self._apply_bakers_dozen(cart.items.values())

    #     else:
    #         print(f"[WARNING] Unrecognized discount type '{self.discount_type}' for discount ID {self.discount_id}")

    #     return total_discount

    # def apply_discount(self, cart):
    #     if self.discount_type == 'external_discount':
    #         return self._apply_external_discount(cart)
    #     elif self.discount_type == 'buy_get_free':
    #         return self._apply_buy_get_free(cart)
    #     elif self.discount_type == 'bakers_dozen':
    #         return self._apply_bakers_dozen(cart.items.values())
    #     else:
    #         print(f"[WARNING] Unrecognized discount type '{self.discount_type}' for discount ID {self.discount_id}")
    #         return 0.0




    # def exclude_free_items(self, item):
    #     """
    #     Calculate the quantity of the item that is still eligible for discount,
    #     excluding quantities that have already been fully discounted.

    #     Args:
    #         item (CartItem): The cart item to evaluate.

    #     Returns:
    #         int: The quantity of the item that is still eligible for discount.
    #     """
        
    #     # Method 1: quantity - sum of sub_cart_items discounted_quantity where discounted_price = 0
    #     eligible_quantity_1 = item.quantity
    #     if item.sub_cart_items:
    #         for sub_item in item.sub_cart_items:
    #             print(f"[DEBUG] Evaluating SubCartItem - sub_cart_id: {sub_item.parent_cart_id}, "
    #                 f"quantity: {sub_item.quantity}, discounted_price: {sub_item.discounted_price}")
    #             if isinstance(sub_item.discounted_price, (int, float)) and sub_item.discounted_price == 0:
    #                 eligible_quantity_1 -= sub_item.quantity
        
    #     # Method 2: non_discounted_quantity + sum of sub_cart_items discounted_quantity where discounted_price > 0
    #     eligible_quantity_2 = item.quantity - item.discounted_quantity
    #     if item.sub_cart_items:
    #         for sub_item in item.sub_cart_items:
    #             print(f"[DEBUG] Evaluating SubCartItem - sub_cart_id: {sub_item.parent_cart_id}, "
    #                 f"quantity: {sub_item.quantity}, discounted_price: {sub_item.discounted_price}")
    #             if isinstance(sub_item.discounted_price, (int, float)) and sub_item.discounted_price > 0:
    #                 eligible_quantity_2 += sub_item.quantity
        
    #     # Check the integrity by comparing both methods
    #     if eligible_quantity_1 == eligible_quantity_2:
    #         return eligible_quantity_1
    #     else:
    #         print(f"[WARNING] Mismatch in eligible quantities: Method 1 = {eligible_quantity_1}, Method 2 = {eligible_quantity_2}")
    #         # Handle discrepancy if needed
    #         return min(eligible_quantity_1, eligible_quantity_2)

    # def exclude_free_items(self, item):
        """
        Calculate the quantity of the item that is still eligible for discount,
        excluding quantities that have already been fully discounted.

        Args:
            item (CartItem): The cart item to evaluate.

        Returns:
            int: The quantity of the item that is still eligible for discount.
        """
        
        # Method 1: quantity - sum of sub_cart_items discounted_quantity where discounted_price = 0
        eligible_quantity_1 = item.quantity
        if item.sub_cart_items:
            eligible_quantity_1 -= sum(
                sub_item.quantity for sub_item in item.sub_cart_items 
                if isinstance(sub_item.discounted_price, (int, float)) and sub_item.discounted_price == 0
            )
        
        # Method 2: non_discounted_quantity + sum of sub_cart_items discounted_quantity where discounted_price > 0
        eligible_quantity_2 = item.quantity - item.discounted_quantity
        if item.sub_cart_items:
            eligible_quantity_2 += sum(
                sub_item.quantity for sub_item in item.sub_cart_items 
                if isinstance(sub_item.discounted_price, (int, float)) and sub_item.discounted_price > 0
            )
        
        # Check the integrity by comparing both methods
        if eligible_quantity_1 == eligible_quantity_2:
            return eligible_quantity_1
        else:
            print(f"[WARNING] Mismatch in eligible quantities: Method 1 = {eligible_quantity_1}, Method 2 = {eligible_quantity_2}")
            # Handle discrepancy if needed
            return min(eligible_quantity_1, eligible_quantity_2)



    # def exclude_free_items(self, item):
        """
        Return a copy of the CartItem with the quantity adjusted by excluding fully discounted items.

        Args:
            item (CartItem): The cart item to evaluate.

        Returns:
            CartItem: A modified copy of the CartItem with adjusted quantity.
        """
        # Create a deep copy of the item to avoid modifying the original object
        item_copy = copy.deepcopy(item)
        
        # Subtract the quantity of fully discounted sub-items from the item quantity
        if item_copy.sub_cart_items:
            for sub_item in item_copy.sub_cart_items:
                print(f"[DEBUG] Evaluating SubCartItem - sub_cart_id: {sub_item.parent_cart_id}, "
                    f"quantity: {sub_item.quantity}, discounted_price: {sub_item.discounted_price}")
                if isinstance(sub_item.discounted_price, (int, float)) and sub_item.discounted_price == 0:
                    item_copy.quantity -= sub_item.quantity
        
        return item_copy


    # def _apply_external_discount(self, cart, remaining_limit):
    #     """Apply an external discount with a fixed amount to eligible items."""
    #     print('Applying external discount')
    #     amount = self.amount
    #     total_discount = 0.0

    #     # Determine the maximum discountable quantity across all eligible items
    #     total_discountable_quantity = 0
    #     eligible_items = []

        # for item in cart.items.values():
        #     if self.is_item_eligible_for_discount(item):
        #         eligible_items.append(item)
        #         total_discountable_quantity += item.quantity

    #     discount_quantity_remaining = min(total_discountable_quantity, self.get_current_limit(cart.customer))

    #     if discount_quantity_remaining <= 0:
    #         return 0.0

    #     # Apply the discount to eligible items, considering the remaining limit and discountable quantity
    #     for item in eligible_items:
    #         if discount_quantity_remaining <= 0:
    #             break

    #         # Calculate the eligible quantity after excluding free items
    #         eligible_quantity = self.exclude_free_items(item)
    #         discount_quantity = min(eligible_quantity, discount_quantity_remaining, remaining_limit)

    #         if discount_quantity > 0:
    #             item.mark_for_discount(discount_quantity, amount, self.discount_id)
    #             discount_quantity_remaining -= discount_quantity
    #             total_discount += discount_quantity * amount
    #             remaining_limit -= discount_quantity

    #         if remaining_limit <= 0:
    #             break

    #     return total_discount




    def exclude_free_items(self, item):
        """
        Returns a modified copy of the CartItem with the quantity reduced by the number of free items,
        and removes those free items from the sub_cart_items.

        Args:
            item (CartItem): The cart item to evaluate.

        Returns:
            CartItem: A new CartItem instance with the quantity adjusted to exclude free items and 
            the corresponding sub_cart_items removed.
        """
        # Create a deep copy of the item to avoid modifying the original
        adjusted_item = copy.deepcopy(item)
        print(f"[DEBUG] exclude_free_items called for {item.product.name}")

        # Initialize adjusted quantity
        adjusted_quantity = adjusted_item.quantity

        # Filter sub_cart_items and adjust the quantity
        filtered_sub_cart_items = []
        print('[DEBUG] item values:', item)
        print(f"[DEBUG] Sub-cart items count: {len(adjusted_item.sub_cart_items)}")

        for sub_item in adjusted_item.sub_cart_items:
            print(f"[DEBUG] Evaluating SubCartItem - sub_cart_id: {sub_item.parent_cart_id}, "
                f"quantity: {sub_item.quantity}, discounted_price: {sub_item.discounted_price}")
            
            # If the discounted price is 0, it's considered free, so reduce the quantity
            if isinstance(sub_item.discounted_price, (int, float)) and sub_item.discounted_price == 0:
                adjusted_quantity -= sub_item.quantity
            else:
                # Keep only the sub_cart_items that are not free
                filtered_sub_cart_items.append(sub_item)
        
        # Update the adjusted item with the new quantity and filtered sub_cart_items
        adjusted_item.quantity = adjusted_quantity
        adjusted_item.sub_cart_items = filtered_sub_cart_items

        return adjusted_item


    def _apply_external_discount(self, cart, remaining_limit):
        """
        Apply a fixed amount external discount to eligible items in the cart.

        This method processes items in the cart to apply an external discount,
        taking into account the remaining customer discount limit and excluding 
        any free items that have already been fully discounted.

        Args:
            cart (Cart): The cart containing items to which the discount should be applied.
            remaining_limit (int): The remaining number of times this discount can be applied 
                                across the cart, taking into account customer limits.

        Returns:
            float: The total discount applied across all eligible items in the cart.
        """
        print('Applying external discount')
        amount = self.amount
        total_discount = 0.0

        # Identify eligible items and calculate the total discountable quantity
        eligible_items = []
        total_discountable_quantity = 0
        for item in cart.items.values():
            if self.is_item_eligible_for_discount(item):
                eligible_items.append(item)
                total_discountable_quantity += item.quantity

        # Determine the maximum discount quantity that can be applied
        discount_quantity_remaining = min(total_discountable_quantity, self.get_current_limit(cart.customer))

        # Return if there is no discount quantity available
        if discount_quantity_remaining <= 0:
            return 0.0

        # Apply the discount to eligible items
        for item in eligible_items:
            if discount_quantity_remaining <= 0 or remaining_limit <= 0:
                break

            # Calculate the discount quantity for this item
            discount_quantity = min(item.quantity, discount_quantity_remaining, remaining_limit)

            if discount_quantity > 0:
                item.mark_for_discount(discount_quantity, amount, self.discount_id)
                discount_quantity_remaining -= discount_quantity
                total_discount += discount_quantity * amount
                remaining_limit -= discount_quantity

        return total_discount


    def _apply_buy_get_free(self, cart, remaining_limit):
        """Apply a 'Buy X, Get Y Free' discount to eligible items in the cart."""
        total_discount = 0.0
        relevant_items = [item for item in cart.items.values() if
                        item.product.system_id in self.buy_items or
                        item.product.upc in self.buy_items or
                        item.product.system_id in self.get_items or
                        item.product.upc in self.get_items]

        relevant_items.sort(key=lambda item: item.product.base_price)
        total_relevant_quantity = sum(item.quantity for item in relevant_items)

        if total_relevant_quantity < self.buy_quantity + self.get_quantity:
            return total_discount

        buy_count = 0
        get_count = 0
        mode = 'buy'

        for item in relevant_items:
            remaining_quantity = item.quantity
            item_id = item.product.system_id or item.product.upc

            while remaining_quantity > 0:
                if mode == 'buy' and item_id in self.buy_items:
                    applicable_buy_quantity = min(self.buy_quantity - buy_count, remaining_quantity)
                    buy_count += applicable_buy_quantity
                    remaining_quantity -= applicable_buy_quantity
                    if buy_count == self.buy_quantity:
                        mode = 'get'

                elif mode == 'get' and item_id in self.get_items:
                    applicable_get_quantity = min(self.get_quantity - get_count, remaining_quantity)
                    get_count += applicable_get_quantity
                    remaining_quantity -= applicable_get_quantity
                    item.mark_for_discount(applicable_get_quantity, item.product.base_price, self.discount_id)
                    total_discount += applicable_get_quantity * item.product.base_price
                    remaining_limit -= applicable_get_quantity

                    if get_count == self.get_quantity:
                        mode = 'buy'
                        buy_count = 0
                        get_count = 0
                if remaining_limit <= 0:
                    print(f"[INFO] Discount limit reached during buy_get_free application.")
                    break

        return total_discount



    # def _apply_buy_get_free(self, cart, remaining_limit):
        """
        Apply a 'Buy X, Get Y Free' discount to eligible items in the cart.

        This method processes eligible items in the cart based on the defined
        buy and get quantities. It sorts items by base price, then applies the
        discount by marking the appropriate quantities as free. The method also
        respects the remaining limit of the discount that can be applied.

        Args:
            cart (Cart): The cart instance containing all items.
            remaining_limit (int): The remaining limit of how many discounts can be applied.

        Returns:
            float: The total discount amount applied to the cart.
        """
        total_discount = 0.0

        # Filter items that are eligible for the buy or get part of the deal
        relevant_items = [item for item in cart.items.values() if
                        item.product.system_id in self.buy_items or
                        item.product.upc in self.buy_items or
                        item.product.system_id in self.get_items or
                        item.product.upc in self.get_items]

        # Sort the relevant items by their base price (cheapest first)
        relevant_items.sort(key=lambda item: item.product.base_price)
        total_relevant_quantity = sum(item.quantity for item in relevant_items)

        # If the total relevant quantity is less than the required buy and get quantity, exit early
        if total_relevant_quantity < self.buy_quantity + self.get_quantity:
            return total_discount

        buy_count = 0
        get_count = 0
        mode = 'buy'

        for item in relevant_items:
            eligible_quantity = self.exclude_free_items(item)
            remaining_quantity = eligible_quantity
            item_id = item.product.system_id or item.product.upc

            while remaining_quantity > 0:
                if mode == 'buy' and item_id in self.buy_items:
                    applicable_buy_quantity = min(self.buy_quantity - buy_count, remaining_quantity)
                    buy_count += applicable_buy_quantity
                    remaining_quantity -= applicable_buy_quantity
                    if buy_count == self.buy_quantity:
                        mode = 'get'

                elif mode == 'get' and item_id in self.get_items:
                    applicable_get_quantity = min(self.get_quantity - get_count, remaining_quantity)
                    get_count += applicable_get_quantity
                    remaining_quantity -= applicable_get_quantity
                    item.mark_for_discount(applicable_get_quantity, item.product.base_price, self.discount_id)
                    total_discount += applicable_get_quantity * item.product.base_price
                    remaining_limit -= applicable_get_quantity

                    if get_count == self.get_quantity:
                        mode = 'buy'
                        buy_count = 0
                        get_count = 0

                if remaining_limit <= 0:
                    print(f"[INFO] Discount limit reached during buy_get_free application.")
                    break

        return total_discount



    # def _apply_buy_get_free(self, cart, remaining_limit):
        """
        Apply a 'Buy X, Get Y Free' discount to eligible items in the cart.

        Args:
            cart (Cart): The cart instance containing all items.
            remaining_limit (int): The remaining limit for this discount application.

        Returns:
            float: The total discount amount applied to the cart.
        """
        total_discount = 0.0
        relevant_items = [item for item in cart.items.values() if
                        item.product.system_id in self.buy_items or
                        item.product.upc in self.buy_items or
                        item.product.system_id in self.get_items or
                        item.product.upc in self.get_items]

        relevant_items.sort(key=lambda item: item.product.base_price)
        total_relevant_quantity = sum(item.quantity for item in relevant_items)

        if total_relevant_quantity < self.buy_quantity + self.get_quantity:
            return total_discount

        buy_count = 0
        get_count = 0
        mode = 'buy'

        for item in relevant_items:
            remaining_quantity = item.quantity
            item_id = item.product.system_id or item.product.upc

            while remaining_quantity > 0:
                if mode == 'buy' and item_id in self.buy_items:
                    applicable_buy_quantity = min(self.buy_quantity - buy_count, remaining_quantity)
                    buy_count += applicable_buy_quantity
                    remaining_quantity -= applicable_buy_quantity
                    if buy_count == self.buy_quantity:
                        mode = 'get'

                elif mode == 'get' and item_id in self.get_items:
                    applicable_get_quantity = min(self.get_quantity - get_count, remaining_quantity)
                    get_count += applicable_get_quantity
                    remaining_quantity -= applicable_get_quantity
                    item.mark_for_discount(applicable_get_quantity, item.product.base_price, self.discount_id)
                    total_discount += applicable_get_quantity * item.product.base_price
                    remaining_limit -= applicable_get_quantity
                    print(f"marking {applicable_get_quantity} of {item.product.short_name} in cart id {item.cart_id} as ineligible for further discounts")
                    item.mark_for_exclusion(applicable_get_quantity)

                    if get_count == self.get_quantity:
                        mode = 'buy'
                        buy_count = 0
                        get_count = 0
                if remaining_limit <= 0:
                    print(f"[INFO] Discount limit reached during buy_get_free application.")
                    break

        return total_discount





    # def _apply_buy_get_free(self, cart, remaining_limit):
        """
        Apply a 'Buy X, Get Y Free' discount to eligible items in the cart.

        Args:
            cart (Cart): The cart instance containing all items.
            remaining_limit (int): The remaining limit for this discount application.

        Returns:
            float: The total discount amount applied to the cart.
        """
        total_discount = 0.0
        relevant_items = [item for item in cart.items.values() if
                        item.product.system_id in self.buy_items or
                        item.product.upc in self.buy_items or
                        item.product.system_id in self.get_items or
                        item.product.upc in self.get_items]

        # Sort relevant items by base price (cheapest first)
        relevant_items.sort(key=lambda item: item.product.base_price)

        # If there are fewer items than required for buy and get, skip discount
        total_relevant_quantity = sum(item.quantity for item in relevant_items)
        if total_relevant_quantity < self.buy_quantity + self.get_quantity:
            return total_discount

        for item in relevant_items:
            buy_count = 0
            get_count = 0
            total_get_count = 0
            remaining_quantity = item.quantity
            item_id = item.product.system_id or item.product.upc

            while remaining_quantity > 0:
                if buy_count < self.buy_quantity and item_id in self.buy_items:
                    # Process buy items, not marking them for exclusion
                    applicable_buy_quantity = min(self.buy_quantity - buy_count, remaining_quantity)
                    buy_count += applicable_buy_quantity
                    remaining_quantity -= applicable_buy_quantity

                elif get_count < self.get_quantity and item_id in self.get_items:
                    # Process get items and mark them for exclusion later
                    applicable_get_quantity = min(self.get_quantity - get_count, remaining_quantity)
                    get_count += applicable_get_quantity
                    remaining_quantity -= applicable_get_quantity
                    item.mark_for_discount(applicable_get_quantity, item.product.base_price, self.discount_id)
                    total_get_count += applicable_get_quantity
                    total_discount += applicable_get_quantity * item.product.base_price
                    remaining_limit -= applicable_get_quantity

                if buy_count == self.buy_quantity and get_count == self.get_quantity:
                    # Reset counters for the next cycle
                    buy_count = 0
                    get_count = 0

                if remaining_limit <= 0:
                    print(f"[INFO] Discount limit reached during buy_get_free application.")
                    break

            # After processing all get items for this cart item, exclude the total get count
            if total_get_count > 0:
                item.mark_for_exclusion(total_get_count)

        return total_discount




    # def _apply_buy_get_free(self, cart, remaining_limit):
        """
        Apply a 'Buy X, Get Y Free' discount to eligible items in the cart.

        Args:
            cart (Cart): The cart instance containing all items.
            remaining_limit (int): The remaining limit for this discount application.

        Returns:
            float: The total discount amount applied to the cart.
        """
        total_discount = 0.0

        # Collect all relevant items that are either in buy_items or get_items
        relevant_items = [item for item in cart.items.values() if
                        item.product.system_id in self.buy_items or
                        item.product.upc in self.buy_items or
                        item.product.system_id in self.get_items or
                        item.product.upc in self.get_items]

        # Sort relevant items by base price (cheapest first)
        relevant_items.sort(key=lambda item: item.product.base_price)

        # Calculate the total quantity of relevant items
        total_relevant_quantity = sum(item.quantity for item in relevant_items)

        # If total quantity is less than the required buy + get, skip the discount
        if total_relevant_quantity < self.buy_quantity + self.get_quantity:
            return total_discount
        
        for i in relevant_items:
            print('relavant item', i)

        # Initialize counters for the buy and get process
        buy_count = 0
        get_count = 0
        total_get_count = 0

        for item in relevant_items:
            remaining_quantity = item.quantity
            item_id = item.product.system_id or item.product.upc

            while remaining_quantity > 0 and remaining_limit > 0:
                if buy_count < self.buy_quantity and item_id in self.buy_items:
                    # Accumulate buy items
                    applicable_buy_quantity = min(self.buy_quantity - buy_count, remaining_quantity)
                    buy_count += applicable_buy_quantity
                    remaining_quantity -= applicable_buy_quantity

                elif get_count < self.get_quantity and item_id in self.get_items:
                    # Accumulate get items and apply the discount
                    applicable_get_quantity = min(self.get_quantity - get_count, remaining_quantity)
                    get_count += applicable_get_quantity
                    remaining_quantity -= applicable_get_quantity
                    item.mark_for_discount(applicable_get_quantity, item.product.base_price, self.discount_id)
                    total_get_count += applicable_get_quantity
                    total_discount += applicable_get_quantity * item.product.base_price
                    remaining_limit -= applicable_get_quantity

                # If we have satisfied the buy-get requirement, reset counters for the next group
                if buy_count == self.buy_quantity and get_count == self.get_quantity:
                    buy_count = 0
                    get_count = 0

            # After processing all get items for this cart item, mark for exclusion
            if total_get_count > 0:
                item.mark_for_exclusion(total_get_count)

            # If remaining limit is reached, stop processing further items
            if remaining_limit <= 0:
                print(f"[INFO] Discount limit reached during buy_get_free application.")
                break

        return total_discount

    def _apply_bakers_dozen(self, cart):
        """
        Apply Baker's Dozen discount logic and return the total discount.

        This method calculates and applies the "Baker's Dozen" discount, where 
        for every set of `buy_quantity` items, the customer receives `get_quantity`
        items for free. It first excludes any already discounted items, then 
        determines the eligible quantity, sorts the items by price, and applies 
        the discount to the lowest-priced items within each cluster.

        Args:
            cart (Cart): The cart instance containing all items.

        Returns:
            float: The total discount amount applied to the cart.
        """

        print("Applying Baker's Dozen Deal")
        total_discount = 0.0

        # Filter eligible items based on the discount's eligible IDs
        eligible_items = [item for item in cart.items.values() if str(item.product.system_id) in self.eligible_ids]

        # Expand items based on their eligible quantity after excluding free items
        expanded_items = []
        for item in eligible_items:
            print('excluded', item.excluded_quantity)
            eligible_quantity = item.quantity - item.excluded_quantity
            print('eligible', eligible_quantity)
            if eligible_quantity > 0:
                expanded_items.extend([item] * eligible_quantity)

        # Sort the expanded items by base price (cheapest first)
        expanded_items.sort(key=lambda x: x.product.base_price)

        print(f"size of eligible_items: {len(expanded_items)}")

        # Calculate the number of full clusters (Baker's Dozen) and apply the discount
        cluster_size = self.buy_quantity + self.get_quantity
        num_clusters = len(expanded_items) // cluster_size

        for i in range(num_clusters):
            cluster = expanded_items[i * cluster_size:(i + 1) * cluster_size]
            min_price_item = min(cluster, key=lambda item: item.product.base_price)
            discount_value = min_price_item.product.base_price
            total_discount += discount_value

            min_price_item.mark_for_discount(1, discount_value, self.discount_id)
            min_price_item.mark_for_exclusion(1)

        return total_discount



    # def _apply_bakers_dozen(self, cart):
    #     """
    #     Apply Baker's Dozen discount logic and return the total discount.

    #     This method calculates and applies the "Baker's Dozen" discount, where 
    #     for every set of `buy_quantity` items, the customer receives `get_quantity`
    #     items for free. It first excludes any already discounted items, then 
    #     determines the eligible quantity, sorts the items by price, and applies 
    #     the discount to the lowest-priced items within each cluster.

    #     Args:
    #         cart (Cart): The cart instance containing all items.

    #     Returns:
    #         float: The total discount amount applied to the cart.
    #     """
    #     total_discount = 0.0

    #     # Filter eligible items based on the discount's eligible IDs
    #     eligible_items = [item for item in cart.items.values() if str(item.product.system_id) in self.eligible_ids]

    #     # Expand items based on their eligible quantity after excluding free items
    #     expanded_items = []
    #     for item in eligible_items:
    #         eligible_quantity = self.exclude_free_items(item)
    #         print(f"[DEBUG] Eligible quantity for {item.product.name}: {eligible_quantity}")
    #         if eligible_quantity > 0:
    #             expanded_items.extend([item] * eligible_quantity)

    #     # Sort the expanded items by base price (cheapest first)
    #     expanded_items.sort(key=lambda x: x.product.base_price)

    #     # Calculate the number of full clusters (Baker's Dozen) and apply the discount
    #     cluster_size = self.buy_quantity + self.get_quantity
    #     num_clusters = len(expanded_items) // cluster_size

    #     for i in range(num_clusters):
    #         cluster = expanded_items[i * cluster_size:(i + 1) * cluster_size]
    #         min_price_item = min(cluster, key=lambda item: item.product.base_price)
    #         discount_value = min_price_item.product.base_price
    #         total_discount += discount_value

    #         # Ensure the discount is applied only once per eligible item, not per individual unit
    #         min_price_item.mark_for_discount(1, discount_value, self.discount_id)

    #     return total_discount

    # def _apply_bakers_dozen(self, cart):
    #     """Apply Baker's Dozen discount logic and return the total discount."""
    #     total_discount = 0.0
    #     eligible_items = [item for item in cart.items.values() if str(item.product.system_id) in self.eligible_ids]

    #     # Expand items based on their eligible quantity after excluding free items
    #     expanded_items = []
    #     for item in eligible_items:
    #         eligible_quantity = self.exclude_free_items(item)
    #         print(f"[DEBUG] Eligible quantity for {item.product.name}: {eligible_quantity}")
    #         if eligible_quantity > 0:
    #             expanded_items.extend([item] * eligible_quantity)

    #     # Sort the expanded items by base price
    #     expanded_items.sort(key=lambda x: x.product.base_price)

    #     # Calculate the number of full clusters (Baker's Dozen) and apply the discount
    #     cluster_size = self.buy_quantity + self.get_quantity
    #     num_clusters = len(expanded_items) // cluster_size

    #     for i in range(num_clusters):
    #         cluster = expanded_items[i * cluster_size:(i + 1) * cluster_size]
    #         min_price_item = min(cluster, key=lambda item: item.product.base_price)
    #         discount_value = min_price_item.product.base_price
    #         total_discount += discount_value
    #         # Ensure the discount is applied only once per eligible item, not per individual unit
    #         min_price_item.mark_for_discount(1, discount_value, self.discount_id)

    #     return total_discount

    # def _apply_bakers_dozen(self, items):
    #     """Apply Baker's Dozen discount logic and return the total discount."""
    #     total_discount = 0.0
    #     eligible_items = [item for item in items if str(item.product.system_id) in self.eligible_ids]

    #     # Expand items based on their eligible quantity after excluding free items
    #     expanded_items = []
    #     for item in eligible_items:
    #         eligible_quantity = self.exclude_free_items(item)
    #         print('eligible quantity', eligible_quantity)
    #         if eligible_quantity > 0:
    #             expanded_items.extend([item] * eligible_quantity)

    #     # Sort the expanded items by base price
    #     expanded_items.sort(key=lambda x: x.product.base_price)

    #     # Calculate the number of full clusters (Baker's Dozen) and apply the discount
    #     cluster_size = self.buy_quantity + self.get_quantity
    #     num_clusters = len(expanded_items) // cluster_size

    #     for i in range(num_clusters):
    #         cluster = expanded_items[i * cluster_size:(i + 1) * cluster_size]
    #         min_price_item = min(cluster, key=lambda item: item.product.base_price)
    #         discount_value = min_price_item.product.base_price
    #         total_discount += discount_value
    #         # Ensure the discount is applied only once per eligible item, not per individual unit
    #         min_price_item.mark_for_discount(1, discount_value, self.discount_id)

    #     return total_discount


    def is_item_eligible_for_discount(self, item):
        """Check if an item is eligible for this discount."""
        return str(item.product.system_id) in self.eligible_ids

    def get_current_limit(self, customer):
        """Get the current limit for the discount based on the customer."""
        # Implement logic to determine how many discounts are available for the customer.
        return self.limit if self.limit else float('inf')

    def add_eligible_ids(self, eligible_ids):
        """Add eligible product IDs to the discount."""
        self.eligible_ids.update(eligible_ids)

    def add_buy_items(self, buy_items):
        """Add buy product IDs to the discount."""
        self.buy_items.update(buy_items)

    def add_get_items(self, get_items):
        """Add get product IDs to the discount."""
        self.get_items.update(get_items)




class Discounts:
    def __init__(self):
        self.discounts = {}
        self.local_limit = {}

    
    def finalize_discount_usage(self, customer):
        """Finalize the discount usage by applying it to the customer."""
        for discount_id, used_limit in self.local_limit.items():
            customer.increment_applied_discount_count(discount_id, used_limit)

        # Clear local limits after finalizing
        self.local_limit.clear()

    def generate_discount_id(self):
        # Placeholder method for generating a unique discount ID
        import uuid
        return str(uuid.uuid4())

    def add_discount(self, discount_id=None, discount_type=None, details=None, buy_quantity=0, get_quantity=0,
                     amount=0.0, strategy=None, strategy_limit=None,
                     lifetime=None, limit=None, discount_taxable=True):
        """Add a discount to the system, with ID generation and duplicate handling."""
        if discount_id is None:
            discount_id = self.generate_discount_id()
            print(f"[INFO] No discount ID provided. Generated ID: {discount_id}")

        if discount_id in self.discounts:
            existing_discount = self.discounts[discount_id]
            print(f"[ERROR] Discount ID {discount_id} already exists.")
            print(f"Existing Discount: {existing_discount}")
            user_input = input(
                f"Do you want to overwrite the existing discount (ID {discount_id})? (yes/no): ").strip().lower()

            if user_input != 'yes':
                print("[INFO] Discarding changes.")
                return
            else:
                print("[INFO] Overwriting existing discount.")

        new_discount = Discount(
            discount_id=discount_id,
            discount_type=discount_type,
            details=details,
            buy_quantity=buy_quantity,
            get_quantity=get_quantity,
            amount=amount,
            strategy=strategy,
            strategy_limit=strategy_limit,
            lifetime=lifetime,
            limit=limit,
            discount_taxable=discount_taxable
        )

        self.discounts[discount_id] = new_discount

    def get_discount_by_id(self, discount_id):
        """
        Retrieve a discount by its ID.

        Args:
            discount_id (str): The unique identifier of the discount.

        Returns:
            Discount: The discount object associated with the given ID, or None if not found.
        """
        return self.discounts.get(discount_id)

    def remove_discount(self, discount_id):
        """
        Remove a discount from the system by its ID.

        Args:
            discount_id (str): The unique identifier of the discount to remove.
        """
        if discount_id in self.discounts:
            del self.discounts[discount_id]
            print(f"[INFO] Discount ID {discount_id} removed.")
        else:
            print(f"[ERROR] Discount ID {discount_id} not found.")


    def apply_discounts(self, cart):
        """Apply all eligible discounts to the cart."""
        total_discount = 0.0
        
        for discount in self.discounts.values():
            # Check if the discount is valid
            if not self._is_discount_valid(discount):
                continue  # Skip invalid or expired discounts

            # Apply the discount to each eligible cart item
            discount_applied = discount.apply_discount(cart)
            if discount_applied:
                total_discount += discount_applied
            else:
                print(f"[WARNING] Discount '{discount.details}' did not apply to any items.")
        
        return total_discount

    # def apply_discounts(self, cart):
    #     """Apply all eligible discounts to the cart."""
    #     for discount in self.discounts.values():
    #         if not self._is_discount_valid(discount):
    #             continue  # Skip invalid or expired discounts

    #         for item in cart.items.values():
    #             if self.is_item_eligible_for_discount(item, discount.discount_id):
    #                 print(f"item {item}")
    #                 print(f"min({item.quantity} - {item.discounted_quantity}, {discount.get_quantity})")
    #                 discount_quantity = min(item.quantity - item.discounted_quantity, discount.get_quantity)
    #                 print(f"outside applying discount of {discount.details}, {discount_quantity} @ {discount.amount}")
    #                 if discount_quantity > 0:
    #                     print(f"applying discount of {discount.details}, {discount_quantity} @ {discount.amount}")
    #                     item.apply_discount(discount.discount_id, discount.amount, discount_quantity)


    def _is_discount_valid(self, discount):
        """Check if a discount is still valid based on its lifetime."""
        if discount.lifetime and datetime.now() > discount.lifetime:
            return False
        return True

    def is_item_eligible_for_discount(self, item, discount_id):
        """Check if the item is eligible for the discount."""
        discount_data = self.discounts.get(discount_id)
        if not discount_data:
            print(f"[ERROR] Discount ID {discount_id} not found.")
            return False

        eligible_ids = discount_data.eligible_ids
        return str(item.product.system_id) in eligible_ids or str(item.product.upc) in eligible_ids




    def get_current_limit(self, customer, discount_id):
        """Get the current limit for the discount based on the customer's usage."""
        if not customer:
            return 0

        # Look up how much of this discount the customer has already used
        used_count = customer.get_applied_discount_count(discount_id)

        if discount_id in self.discounts:
            total_limit = self.discounts[discount_id].limit
            if total_limit is None:
                return float('inf')  # Treat as unlimited
            return max(0, total_limit - used_count)
        return 0




    # def get_current_limit(self, customer, discount_id):
    #     if not customer:
    #         return 0
    #     """Check and return the current limit for a discount based on the customer's usage."""
    #     used_count = customer.get_applied_discount_count(discount_id)
    #     if discount_id in self.discounts:
    #         total_limit = self.discounts[discount_id]['limit']
    #         if total_limit is None:
    #             return float('inf')  # Treat as unlimited
    #         return max(0, total_limit - used_count)
    #     return 0

    def mark_discount(self, cart, discount_id):
        """Mark discount for eligible items in the cart based on the current limit."""
        for item in cart.items.values():
            current_limit = self.get_current_limit(cart.customer, discount_id)
            if current_limit <= 0:
                continue  # Skip items if no discount is available

            if self.is_item_eligible_for_discount(item, discount_id):
                discount_quantity = min(item.quantity, current_limit)
                item.mark_for_discount(discount_quantity, self.discounts[discount_id]['amount'], discount_id)
                cart.customer.increment_applied_discount_count(discount_id, discount_quantity)
                self.local_limit[discount_id] = self.get_current_limit(cart.customer, discount_id)  # Update after discount application

    def finalize_discount_usage(self, customer):
        """Finalize the discount usage by applying it to the customer."""
        for discount_id, used_limit in self.local_limit.items():
            customer.increment_applied_discount_count(discount_id, used_limit)

    def undo_discount_usage(self, customer, discount_id, quantity):
        """Undo discount usage for returns, updating the customer's limit."""
        customer.decrement_applied_discount_count(discount_id, quantity)


    def add_eligible_products_from_csv(self, discount_id, csv_path):
        """Add eligible products to a specific discount from a CSV file."""
        if discount_id not in self.discounts:
            raise ValueError(f"Discount ID {discount_id} does not exist.")

        discount = self.discounts[discount_id]

        df = pd.read_csv(csv_path, dtype=str)

        if 'System ID' in df.columns:
            eligible_ids = df['System ID'].dropna().unique()
        elif 'UPC' in df.columns:
            eligible_ids = df['UPC'].dropna().unique()
        else:
            raise ValueError("CSV must contain 'System ID' or 'UPC' column.")

        discount.add_eligible_ids(eligible_ids)

    def add_eligible_products(self, discount_id, eligible_ids):
        """Add eligible product IDs for a specific discount."""
        if discount_id not in self.discounts:
            raise ValueError(f"Discount ID {discount_id} does not exist.")

        # Get the Discount object
        discount = self.discounts[discount_id]

        # Update the eligible_ids in the Discount object
        discount.add_eligible_ids(eligible_ids)

    def add_discounts_from_csv(self, csv_path):
        """Load and add multiple discounts from a CSV file."""
        df = pd.read_csv(csv_path, dtype=str)

        # Dictionary to track the generated discount IDs for each unique discount name
        discount_name_to_id = {}

        for _, row in df.iterrows():
            # Extract the relevant fields from the row
            discount_name = row.get('Discount Name')
            discount_type = row.get('Type')
            details = discount_name
            amount_str = row.get('Discount')
            amount = float(amount_str) if pd.notna(amount_str) else 0.0

            # Handle the 'Limit' column, converting it to an integer if valid, or None if it's null
            limit_str = row.get('Limit')
            limit = None if pd.isna(limit_str) else int(float(limit_str))

            lifetime = row.get('Lifetime', None)
            discount_taxable = row.get('Discount Taxable', 'True').lower() == 'true'
            system_id = row.get('System ID')
            upc = row.get('UPC')

            # Check for Buy, Get, Buy Items, and Get Items columns
            buy_quantity_str = row.get('Buy')
            buy_quantity = int(buy_quantity_str) if pd.notna(buy_quantity_str) else 0
            get_quantity_str = row.get('Get')
            get_quantity = int(get_quantity_str) if pd.notna(get_quantity_str) else 0
            buy_items_str = row.get('Buy Items')
            get_items_str = row.get('Get Items')

            # Parse buy_items and get_items if they are present
            buy_items = self._parse_list_column(buy_items_str) if buy_items_str else []
            get_items = self._parse_list_column(get_items_str) if get_items_str else []


            # Use the existing discount ID if the discount name has already been processed
            if discount_name not in discount_name_to_id:
                discount_id = self.generate_discount_id()
                discount_name_to_id[discount_name] = discount_id

                # Add the new discount
                self.add_discount(
                    discount_id=discount_id,
                    discount_type=discount_type,
                    details=details,
                    buy_quantity=buy_quantity,
                    get_quantity=get_quantity,
                    amount=amount,
                    limit=limit,
                    lifetime=lifetime,
                    discount_taxable=discount_taxable
                )
            else:
                discount_id = discount_name_to_id[discount_name]

            # Determine the eligible IDs (either System ID or UPC) and add them
            eligible_ids = []
            if system_id and pd.notna(system_id):
                eligible_ids.append(system_id)
            if upc and pd.notna(upc):
                eligible_ids.append(upc)

            # Add eligible products for buy and get items if applicable
            if buy_items:
                self.add_buy_items(discount_id, buy_items)
            if get_items:
                self.add_get_items(discount_id, get_items)

            # Also handle older format where eligible products are directly listed
            if eligible_ids:
                # Assume that if eligible_ids are provided directly, they belong to either buy_items or get_items
                if discount_type == 'buy_get_free':
                    # If it's a buy x get y free discount, distribute eligible_ids accordingly
                    if buy_quantity > 0:
                        self.add_buy_items(discount_id, eligible_ids)
                    if get_quantity > 0:
                        self.add_get_items(discount_id, eligible_ids)
                else:
                    # For other discount types, use eligible_ids as a general list (if applicable)
                    self.add_eligible_products(discount_id, eligible_ids)

    def add_buy_items(self, discount_id, buy_items):
        """Add eligible buy product IDs for a specific discount."""
        if discount_id not in self.discounts:
            raise ValueError(f"Discount ID {discount_id} does not exist.")

        # Get the Discount object
        discount = self.discounts[discount_id]

        # Ensure the buy_items set exists and update it
        if not hasattr(discount, 'buy_items') or discount.buy_items is None:
            discount.buy_items = set()

        discount.add_buy_items(buy_items)

    def add_get_items(self, discount_id, get_items):
        """Add eligible get product IDs for a specific discount."""
        if discount_id not in self.discounts:
            raise ValueError(f"Discount ID {discount_id} does not exist.")

        # Get the Discount object
        discount = self.discounts[discount_id]

        # Ensure the get_items set exists and update it
        if not hasattr(discount, 'get_items') or discount.get_items is None:
            discount.get_items = set()

        discount.add_get_items(get_items)

    def _parse_list_column(self, column_value):
        """Parse a list column that might be in string format or list format."""
        if pd.isna(column_value):
            return []

        # Attempt to convert to list
        try:
            return ast.literal_eval(column_value)
        except (ValueError, SyntaxError):
            # If not a valid list, assume it's a single item wrapped in a list
            return [column_value]



    def add_discounts_from_list(self, discounts_list):
        """Add multiple discounts from a list of dictionaries."""
        for discount_data in discounts_list:
            discount_id = discount_data['discount_id']
            discount_type = discount_data['type']
            details = discount_data['details']
            amount = discount_data['amount']
            limit = discount_data['limit']
            lifetime = discount_data.get('lifetime', None)
            discount_taxable = discount_data.get('taxable', True)
            eligible_ids = discount_data['eligible_ids']

            self.add_discount(
                discount_id=discount_id,
                discount_type=discount_type,
                details=details,
                amount=amount,
                limit=limit,
                lifetime=lifetime,
                discount_taxable=discount_taxable
            )
            self.add_eligible_products(discount_id, eligible_ids)


    def _apply_buy_get_free(self, cart, discount_data):
        """Apply a 'Buy X, Get Y Free' discount to eligible items in the cart."""
        total_discount = 0.0
        buy_quantity = discount_data['buy_quantity']
        get_quantity = discount_data['get_quantity']
        buy_items = discount_data['buy_items']
        get_items = discount_data['get_items']
        discount_id = discount_data['discount_id']

        # Check if the discount applies to this customer
        current_limit = self.get_current_limit(cart.customer, discount_id)
        if current_limit <= 0:
            print(f"[DEBUG] No remaining discount limit for customer on discount ID {discount_id}.")
            return total_discount

        # Combine buy and get items since items can be in both
        relevant_items = [item for item in cart.items.values() if
                          item.product.system_id in buy_items or item.product.upc in buy_items or
                          item.product.system_id in get_items or item.product.upc in get_items]

        # Sort relevant items by price (cheapest first)
        relevant_items.sort(key=lambda item: item.product.base_price)

        # Calculate total quantity of relevant items in the cart
        total_relevant_quantity = sum(item.quantity for item in relevant_items)

        # If the total relevant quantity is less than buy_quantity + get_quantity, do not apply the discount
        if total_relevant_quantity < buy_quantity + get_quantity:
            print(f"[DEBUG] Not enough items to qualify for the discount on discount ID {discount_id}.")
            return total_discount

        # Initialize counters
        buy_count = 0
        get_count = 0
        mode = 'buy'  # Start with counting towards buy_quantity

        # Process each item in the sorted list
        for item in relevant_items:
            remaining_quantity = item.quantity  # Copy the item's quantity to track usage separately
            item_id = item.product.system_id or item.product.upc

            while remaining_quantity > 0:
                if mode == 'buy':
                    if item_id in buy_items:  # Only count if the item is in buy_items
                        # Count towards buy_quantity
                        applicable_buy_quantity = min(buy_quantity - buy_count, remaining_quantity)
                        buy_count += applicable_buy_quantity
                        remaining_quantity -= applicable_buy_quantity

                        # If buy_quantity is reached, switch to counting towards get_quantity
                        if buy_count == buy_quantity:
                            mode = 'get'

                elif mode == 'get':
                    if item_id in get_items:  # Only count if the item is in get_items
                        # Count towards get_quantity
                        applicable_get_quantity = min(get_quantity - get_count, remaining_quantity)
                        get_count += applicable_get_quantity
                        remaining_quantity -= applicable_get_quantity

                        # Mark the item for discount if part of the get_quantity
                        item.mark_for_discount(applicable_get_quantity, item.product.base_price, discount_id)
                        total_discount += applicable_get_quantity * item.product.base_price

                        # If get_quantity is reached, switch back to counting towards buy_quantity
                        if get_count == get_quantity:
                            mode = 'buy'
                            buy_count = 0  # Reset buy_count for the next cycle
                            get_count = 0  # Reset get_count for the next cycle

        return total_discount


    def _alert_missing_get_items(self, get_items):
        """Print an alert that adding certain items will activate the discount."""
        get_item_names = [item.product.short_name for item in get_items]
        item_list_str = ', '.join(get_item_names)
        print(f"[ALERT] Add any of the following items to activate the discount: {item_list_str}")



    def _apply_bakers_dozen(self, items, buy_quantity, get_quantity, eligible_ids):
        """Apply Baker's Dozen discount logic and return the total discount."""
        total_discount = 0.0

        # Filter eligible items
        eligible_items = [item for item in items if str(item.product.system_id) in eligible_ids]

        # Prepare a list of products by expanding their quantities
        expanded_items = []
        for item in eligible_items:
            expanded_items.extend([item] * item.quantity)

        # Sort the expanded items list by base price
        expanded_items = sorted(expanded_items, key=lambda x: x.product.base_price)

        # Calculate the number of full clusters
        total_items = len(expanded_items)
        num_clusters = total_items // (buy_quantity + get_quantity)

        # Apply the discount for each full cluster
        for i in range(num_clusters):
            cluster = expanded_items[i * (buy_quantity + get_quantity):(i + 1) * (buy_quantity + get_quantity)]
            # Identify the item with the lowest price in the cluster
            min_price_item = min(cluster, key=lambda item: item.product.base_price)
            discount_value = min_price_item.product.base_price
            total_discount += discount_value

            # Mark the item with the lowest price for a full discount
            min_price_item.mark_for_discount(1, discount_value, discount_id=1)

            print(
                f"[DEBUG] Marked 1 free item of {min_price_item.product.short_name} for a discount of {discount_value:.2f}, total discount: {total_discount:.2f}")

        # Handle alerts for the next potential free item
        remaining_items = total_items % (buy_quantity + get_quantity)
        items_needed_for_next_discount = (buy_quantity + get_quantity) - remaining_items

        # Alerts start showing when 9, 10, or 11 items are added after the last free item was given
        if remaining_items >= buy_quantity - 3:
            if items_needed_for_next_discount == 1:
                print(f"[ALERT] Add 1 more can to get 1 can for free!")
            else:
                print(f"[ALERT] Add {items_needed_for_next_discount} more cans to get 1 can for free!")

        return total_discount



    def _select_free_items(self, items, count, strategy, limit=None):
        """Select free items based on the strategy."""
        if strategy == 'lowest_price':
            sorted_items = sorted(items, key=lambda x: x.product.base_price)
        elif strategy == 'highest_price':
            sorted_items = sorted(items, key=lambda x: x.product.base_price, reverse=True)
        elif strategy == 'average_price':
            average_price = sum(item.product.base_price for item in items) / len(items)
            sorted_items = sorted(items, key=lambda x: abs(x.product.base_price - average_price))
        elif strategy == 'predefined':
            if limit:
                sorted_items = [item for item in items if item.product.system_id in limit or item.product.upc in limit]
            else:
                sorted_items = []
                print("[WARNING] No limit provided for predefined strategy, returning an empty list.")
        else:
            print(f"[WARNING] Unknown strategy '{strategy}', returning items as-is.")
            sorted_items = items

        # Apply price limit filtering if applicable
        if limit and strategy in ['lowest_price', 'highest_price', 'average_price']:
            sorted_items = [item for item in sorted_items if
                            abs(item.product.base_price - sorted_items[0].product.base_price) <= limit]

        return sorted_items[:count]

