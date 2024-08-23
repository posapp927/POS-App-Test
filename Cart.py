from Customer import Customer
from Discounts import Discounts
from Product import Product

class CartItem:
    def __init__(self, cart_id, product, cart, quantity=1):
        """
        Initialize a CartItem instance.

        Args:
            cart_id (str): Unique identifier for the cart item.
            product (Product): An instance of the Product class representing the item.
            quantity (int): The quantity of the item in the cart (default is 1).
            cart (Cart): An instance of the Cart class this item belongs to.
        """
        if cart is None:
            raise ValueError("CartItem must be associated with a Cart instance.")

        self.cart_id = cart_id
        self.product = product
        self.quantity = quantity
        self.discounted_quantity = 0
        self.discount_ids = set()
        self.total_discount_amount = 0.0
        self.discounted_price = product.base_price
        self.sub_cart_items = []  # For managing different discounts on the same item
        self.cart = cart
        self.excluded_quantity = 0  # Add this attribute to track excluded items

    def mark_for_exclusion(self, quantity):
        """
        Mark a specific quantity of this item as excluded from further discounts.
        
        Args:
            quantity (int): The number of items to exclude.
        """
        print(f"incrementing excluded quantity for {self.cart_id}, {self.product.short_name} from {self.excluded_quantity} to {self.excluded_quantity + quantity}")
        self.excluded_quantity += quantity

    def is_excluded(self, quantity):
        """
        Check if a specific quantity of this item is excluded from discounts.
        
        Args:
            quantity (int): The number of items to check.
            
        Returns:
            bool: True if the quantity is fully excluded, False otherwise.
        """
        return quantity <= self.excluded_quantity

    def increase_quantity(self, amount=1):
        """
        Increase the quantity of the item in the cart.

        Args:
            amount (int): The amount to increase the quantity by (default is 1).
        """
        self.quantity += amount
        print(f"[DEBUG] Increased quantity of {self.product.short_name} by {amount}. New quantity: {self.quantity}")

    def add_quantity(self, amount=1):
        """
        Increase the quantity of the cart item.

        Args:
            amount (int): The amount to increase the quantity by (default is 1).
        """
        self.quantity += amount

    def remove_quantity(self, amount=1):
        """
        Decrease the quantity of the cart item.

        Args:
            amount (int): The amount to decrease the quantity by (default is 1).

        Raises:
            ValueError: If the amount to remove exceeds the current quantity.
        """
        if amount > self.quantity:
            raise ValueError("Cannot remove more items than present in the cart.")
        self.quantity -= amount

    def initialize_discount_attributes(self):
        """
        Initialize discount-related attributes if they are not already initialized.
        """
        if self.discounted_quantity is None:
            self.discounted_quantity = 0
        if self.discount_ids is None:
            self.discount_ids = []
        if self.total_discount_amount is None:
            self.total_discount_amount = 0.0
        if self.discounted_price is None:
            self.discounted_price = self.product.base_price

    def reset_discounts(self):
        """
        Reset all discounts applied to this CartItem.
        """
        self.discounted_quantity = 0
        self.discount_ids = []
        self.total_discount_amount = 0.0
        self.discounted_price = self.product.base_price

        # If there are any sub-cart items, reset their discounts as well
        self.sub_cart_items.clear()

        print(f"[DEBUG] Reset all discounts for {self.product.short_name}")

    def mark_for_discount(self, discount_quantity, discount_value, discount_id):
        """
        Mark a specific quantity of this item as discounted.

        Args:
            discount_quantity (int): The number of items to discount.
            discount_value (float): The discount amount to apply per item.
            discount_id (str): The ID of the discount being applied.
        """
        if discount_quantity > self.quantity - self.discounted_quantity:
            raise ValueError("Cannot discount more items than available.")

        # Update the discounted quantity and discount amount
        self.discounted_quantity += discount_quantity
        self.total_discount_amount += discount_quantity * discount_value
        self.discount_ids.append(discount_id)

        # Recalculate the discounted price
        self.discounted_price = max(self.product.base_price - (self.total_discount_amount / self.discounted_quantity), 0.0)
        print(f"discount_ids: {self.discount_ids}\n discounted_quantity: ")
        for discount_id in self.discount_ids:
            print(f"{self.cart.discounts.get_discount_by_id(discount_id).details}")
        print(f"{self.discounted_quantity}\n total_discount_amount: {self.total_discount_amount}\n"
              f"-------------------------------------------------------------------------\n")

        print(f"[DEBUG] Marked {discount_quantity} items for discount with ID {discount_id} at {discount_value} each.")

        print(f'Updating subcart with {discount_id}, {discount_value}, {discount_quantity}')
        # Create or update a sub-cart item if needed
        self._update_or_create_sub_cart_item(discount_id, discount_value, discount_quantity)

    # def apply_discount(self, discount_id, discount_amount, quantity):
    #     """
    #     Apply a discount to a specific quantity of the cart item.

    #     Args:
    #         discount_id (str): The unique identifier of the discount.
    #         discount_amount (float): The discount amount to apply per item.
    #         quantity (int): The quantity to which the discount is applied.

    #     Raises:
    #         ValueError: If trying to apply a discount to more items than available.
    #     """
    #     if quantity > self.quantity - self.discounted_quantity:
    #         raise ValueError("Cannot apply discount to more items than available.")

    #     self.discounted_quantity += quantity
    #     self.total_discount_amount += discount_amount * quantity
    #     self.discount_ids.append(discount_id)
    #     self.discounted_price = max(self.product.base_price - discount_amount, 0.0)
    #     print(f"apply_discount discount_ids: {self.discount_ids}\n discounted_quantity: ")
    #     for discount_id in self.discount_ids:
    #         print(f"apply_discount {self.cart.discounts.get_discount_by_id(discount_id).details}")
    #     print(f"apply_discount {self.discounted_quantity}\n total_discount_amount: {self.total_discount_amount}\n"
    #           f"-------------------------------------------------------------------------\n")

    #     print(f"apply_discount [DEBUG] Marked {quantity} items for discount with ID {discount_id} at {discount_amount} each.")

    #     # Create or update a sub-cart item if needed
    #     self._update_or_create_sub_cart_item(discount_id, discount_amount, quantity)

    def _update_or_create_sub_cart_item(self, discount_id, discount_amount, quantity):
        """
        Update an existing sub-cart item or create a new one.

        Args:
            discount_id (str): The discount ID to associate with the sub-cart item.
            discount_amount (float): The discount amount per item.
            quantity (int): The quantity of items to be included in the sub-cart item.
        """

        print('creating sub cart item')
        # Find if a sub-cart item with the same discount exists
        for sub_item in self.sub_cart_items:
            if sub_item.discounted_price == self.discounted_price and discount_id in sub_item.discount_ids:
                sub_item.quantity += quantity
                return

        # If no matching sub-cart item is found, create a new one
        new_sub_item = SubCartItem(
            parent_cart_id=self.cart_id,
            product=self.product,
            quantity=quantity,
            discount_ids=[discount_id],
            discount_amount=discount_amount,
            discounted_price=self.discounted_price,
            cart=self.cart
        )
        print('new_sub_item', new_sub_item)
        self.sub_cart_items.append(new_sub_item)
        for i in self.sub_cart_items:
            print('appended new_sub_item', i)

    def calculate_subtotal(self):
        """
        Calculate the subtotal for the cart item.

        Returns:
            float: The subtotal, considering both discounted and non-discounted items.
        """
        non_discounted_subtotal = (self.quantity - self.discounted_quantity) * self.product.base_price
        discounted_subtotal = sum(sub_item.calculate_subtotal() for sub_item in self.sub_cart_items)
        return non_discounted_subtotal + discounted_subtotal

    def calculate_taxable_total(self):
        """
        Calculate the taxable total for the cart item.

        Returns:
            float: The taxable total.
        """
        return self.calculate_subtotal() * self.cart.tax_rate  # Use the Cart's tax rate

    def calculate_total(self):
        """
        Calculate the final total for the cart item, including tax.

        Returns:
            float: The total price of the cart item.
        """
        return self.calculate_subtotal() + self.calculate_taxable_total()  # Use the Cart's tax rate

    def __str__(self):
        sub_cart_info = ""
        if self.sub_cart_items:
            sub_cart_info = "\n  Sub-Cart Items:\n"
            for sub_item in self.sub_cart_items:
                sub_cart_info += f"    SubCartItem(parent_cart_id={sub_item.parent_cart_id}, quantity={sub_item.quantity}, discounted_price={sub_item.discounted_price:.2f}, discount_ids={sub_item.discount_ids})\n"

        return (
            f"CartItem(cart_id={self.cart_id}, "
            f"product_name={self.product.name}, "
            f"brand={self.product.brand}, "
            f"size={self.product.size}, "
            f"quantity={self.quantity}, "
            f"discounted_quantity={self.discounted_quantity}, "
            f"discount_ids={self.discount_ids}, "
            f"total_discount_amount={self.total_discount_amount:.2f}, "
            f"discounted_price={self.discounted_price:.2f}, "
            f"subtotal={self.calculate_subtotal():.2f}, "
            f"taxable_total={self.calculate_taxable_total():.2f}, "
            f"total={self.calculate_total():.2f})"
            f"sub_cart_items={sub_cart_info}"
        )




class SubCartItem:
    def __init__(self, parent_cart_id, product, quantity, discount_ids, discounted_price, discount_amount, cart):
        """
        Initialize a SubCartItem instance.

        Args:
            parent_cart_id (str): The cart ID of the parent CartItem.
            product (Product): An instance of the Product class representing the item.
            quantity (int): The quantity of items in this sub-cart item.
            discount_ids (list): A list of discount IDs applied to this sub-cart item.
            discounted_price (float): The price after applying the discounts.
            cart (Cart): An instance of the Cart class this item belongs to.
        """
        if cart is None:
            raise ValueError("CartItem must be associated with a Cart instance.")
        self.parent_cart_id = parent_cart_id
        self.product = product
        self.quantity = quantity
        self.discount_ids = discount_ids
        self.discounted_price = discounted_price
        self.discount_amount = discount_amount
        self.cart = cart
        self.sub_cart_id = f"sub_{self.parent_cart_id}_{hash(self)}"  # Add unique sub_cart_id

    # Other methods remain unchanged...

    def add_quantity(self, amount=1):
        """
        Increase the quantity of the sub-cart item.

        Args:
            amount (int): The amount to increase the quantity by (default is 1).
        """
        self.quantity += amount

    def remove_quantity(self, amount=1):
        """
        Decrease the quantity of the sub-cart item.

        Args:
            amount (int): The amount to decrease the quantity by (default is 1).

        Raises:
            ValueError: If the amount to remove exceeds the current quantity.
        """
        if amount > self.quantity:
            raise ValueError("Cannot remove more items than present in the sub-cart item.")
        self.quantity -= amount

    def calculate_subtotal(self):
        """
        Calculate the subtotal for this sub-cart item.

        Returns:
            float: The subtotal for the discounted items in this sub-cart item.
        """
        return self.quantity * self.discounted_price

    def calculate_taxable_total(self):
        """
        Calculate the taxable total for this sub-cart item.

        Returns:
            float: The taxable total for this sub-cart item.
        """
        return self.calculate_subtotal() * self.cart.tax_rate  # Use the Cart's tax rate

    def calculate_total(self):
        """
        Calculate the final total for this sub-cart item, including tax.

        Returns:
            float: The total price of this sub-cart item.
        """
        return self.calculate_subtotal() + self.calculate_taxable_total()  # Use the Cart's tax rate

    def __str__(self):
        return f"SubCartItem(parent_cart_id={self.parent_cart_id}, product={self.product.name}, quantity={self.quantity}, discounted_price={self.discounted_price:.2f}, sub_cart_id={self.sub_cart_id})"



class Cart:
    def __init__(self, customer=None, tax_rate=0.0, discounts=None):
        """
        Initialize a Cart instance.

        Args:
            customer (Optional): The customer associated with the cart.
            tax_rate (float): The tax rate to apply to the cart's items.
            discounts (Discounts): An instance of the Discounts class to manage applicable discounts.
        """
        self.items = {}  # Dictionary to hold CartItem instances, keyed by cart_id
        self.customer = customer  # The customer associated with the cart
        self.tax_rate = tax_rate  # Tax rate to apply to items in the cart
        self.discounts = discounts  # Instance of Discounts class for managing discounts
        self.log = []  # List to keep a log of cart interactions
        self.next_cart_id = 1  # A counter to generate unique cart IDs

    def set_customer(self, customer):
        """
        Associate a customer with the cart.

        Args:
            customer (Customer): An instance of the Customer class to associate with this cart.
        """
        if not isinstance(customer, Customer):
            raise ValueError("Expected a Customer instance.")

        self.customer = customer
        print(f"[DEBUG] Customer {customer.first_name} {customer.last_name} set for the cart.")


    def _generate_cart_id(self):
        """
        Generate a unique cart ID for a new cart item.

        Returns:
            str: A unique cart ID.
        """
        cart_id = f"cart_{self.next_cart_id}"
        self.next_cart_id += 1
        return cart_id

    def log_action(self, action, details):
        """
        Log an action performed on the cart.

        Args:
            action (str): The action performed (e.g., "add", "remove", "update").
            details (str): Details about the action.
        """
        self.log.append(f"{action}: {details}")


    def add_item(self, product, quantity=1):
        """
        Add a product to the cart or update the quantity if it already exists.

        Args:
            product (Product): An instance of the Product class representing the item.
            quantity (int): The quantity of the item to add (default is 1).
        """
        if product is None:
            raise ValueError("Cannot add a NoneType product to the cart.")

        print(f'Adding {quantity} of {product.short_name}')

        # Determine if the product is already in the cart
        existing_item = None
        for item in self.items.values():
            if item.product.system_id == product.system_id:
                existing_item = item
                break

        if existing_item:
            # If the item is already in the cart, update its quantity
            existing_item.increase_quantity(quantity)
        else:
            # Generate a new cart ID for the new item
            cart_id = self._generate_cart_id()

            # Add the new CartItem to the cart
            new_item = CartItem(cart_id, product, self, quantity)
            self.items[cart_id] = new_item

        # Apply discounts dynamically after adding an item
        if self.discounts:
            self.apply_discounts()

        # Log the action
        self.log_action("add", f"Added {quantity} of {product.short_name} to the cart")


    def apply_discounts(self):
        """
        Apply discounts to all items in the cart using the Discounts instance.
        """
        if not self.discounts:
            return

        # Reset all discounts on items before reapplying
        for item in self.items.values():
            item.reset_discounts()

        # Apply discounts from the Discounts instance
        self.discounts.apply_discounts(self)

        # Log the action of applying discounts
        self.log_action("apply_discounts", "Applied discounts to cart items")


    def get_cart_items(self):
        """
        Retrieve a summary of all items in the cart, including detailed information.

        Returns:
            list: A list of dictionaries, each containing detailed information about a cart item.
        """
        cart_summary = []

        for cart_item in self.items.values():
            # Initialize discount attributes if not already initialized
            cart_item.initialize_discount_attributes()

            # Basic product information
            item_summary = {
                'cart_id': cart_item.cart_id,
                'product_name': cart_item.product.name,
                'product_short_name': cart_item.product.short_name,
                'brand': cart_item.product.brand,
                'size': cart_item.product.size,
                'category': cart_item.product.category,
                'pets': cart_item.product.pets,
                'system_id': cart_item.product.system_id,
                'upc': cart_item.product.upc,
                'quantity': cart_item.quantity,
                'discounted_quantity': cart_item.discounted_quantity,
                'non_discounted_quantity': cart_item.quantity - cart_item.discounted_quantity,
                'base_price': cart_item.product.base_price,
                'discounted_price': cart_item.discounted_price,
                'total_discount_amount': cart_item.total_discount_amount,
            }

            # Pricing information
            subtotal = cart_item.quantity * cart_item.product.base_price
            discount_total = cart_item.discounted_quantity * (cart_item.product.base_price - cart_item.discounted_price)

            # Adjust this to correctly handle discount objects
            discount_objects = [self.discounts.get_discount_by_id(d_id) for d_id in cart_item.discount_ids]
            taxable_total = subtotal - discount_total if self.discounts and any(
                discount.discount_taxable for discount in discount_objects) else subtotal

            tax = taxable_total * self.tax_rate
            total = subtotal + tax - discount_total


            

            # Add pricing and discount information to the summary
            item_summary.update({
                'subtotal': subtotal,
                'taxable_total': taxable_total,
                'tax': tax,
                'total': total,
                'discount_ids': cart_item.discount_ids,
                'discount_total': discount_total,
            })

            # Handle sub-cart items if they exist
            if cart_item.sub_cart_items:
                sub_items_summary = []
                for sub_item in cart_item.sub_cart_items:
                    sub_summary = {
                        'parent_cart_id': sub_item.parent_cart_id,
                        'sub_cart_id': sub_item.sub_cart_id,
                        'discounted_quantity': sub_item.quantity,
                        'discounted_price': sub_item.discounted_price,
                        'discount_ids': sub_item.discount_ids,
                        'subtotal': sub_item.quantity * sub_item.discounted_price,
                    }
                    sub_items_summary.append(sub_summary)
                    print('sub_cart_item summary', sub_items_summary)
                item_summary['sub_cart_items'] = sub_items_summary

            cart_summary.append(item_summary)

        return cart_summary

