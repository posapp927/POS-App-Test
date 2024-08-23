import logging
from datetime import datetime
from typing import List, Dict, Optional, Union

# Setup the logger for this module
logger = logging.getLogger('custom_discounts.core.discount')

class Discount:
    def __init__(self, discount_id: str, discount_type: Optional[str] = None, details: Optional[str] = None,
                 buy_quantity: int = 0, get_quantity: int = 0, amount: float = 0.0, strategy: Optional[str] = None,
                 strategy_limit: Optional[int] = None, lifetime: Optional[Union[str, List[str]]] = None,
                 limit: Optional[int] = None, discount_taxable: bool = True):
        """
        Represents a discount with specific rules and limits.

        Args:
            discount_id (str): Unique identifier for the discount.
            discount_type (str): Type of the discount (e.g., "percentage", "fixed").
            details (str): Description of the discount.
            buy_quantity (int): Quantity required to qualify for the discount.
            get_quantity (int): Quantity given for free or at a discount.
            amount (float): The discount amount.
            strategy (str): Strategy used for applying the discount.
            strategy_limit (int): Maximum times the strategy can be applied.
            lifetime (str or List[str]): Lifetime of the discount (can be a single date or a range).
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

        # Parse the lifetime into datetime objects
        self.lifetime = self.parse_lifetime(lifetime)

        logger.info(f"Initialized Discount: {self}")

    @staticmethod
    def parse_lifetime(lifetime: Optional[Union[str, List[str]]]) -> Optional[Union[datetime, tuple]]:
        """
        Parse the lifetime argument into datetime objects.

        Args:
            lifetime (str or List[str]): Lifetime in the format 'MM/DD/YYYY' or a list representing a range.

        Returns:
            datetime or tuple: Parsed lifetime or range of lifetimes as datetime objects.
        """
        if isinstance(lifetime, str):
            try:
                return datetime.strptime(lifetime, '%m/%d/%Y')
            except ValueError:
                logger.error(f"Invalid date format for lifetime: {lifetime}. Expected MM/DD/YYYY.")
                return None
        elif isinstance(lifetime, list) and len(lifetime) == 2:
            try:
                return (datetime.strptime(lifetime[0], '%m/%d/%Y'), datetime.strptime(lifetime[1], '%m/%d/%Y'))
            except ValueError:
                logger.error(f"Invalid date range for lifetime: {lifetime}. Expected MM/DD/YYYY.")
                return None
        return None

    def is_active(self) -> bool:
        """
        Check if the discount is currently active based on its lifetime.

        Returns:
            bool: True if the discount is active, False otherwise.
        """
        if isinstance(self.lifetime, tuple):
            start, end = self.lifetime
            is_active = start <= datetime.now() <= end
            logger.debug(f"Discount {self.discount_id} is_active check: {is_active}")
            return is_active
        elif isinstance(self.lifetime, datetime):
            is_active = datetime.now() <= self.lifetime
            logger.debug(f"Discount {self.discount_id} is_active check: {is_active}")
            return is_active
        return True

    def add_eligible_ids(self, eligible_ids: List[str]):
        """
        Add eligible product IDs to the discount.

        Args:
            eligible_ids (List[str]): List of product IDs eligible for the discount.
        """
        self.eligible_ids.update(eligible_ids)
        logger.debug(f"Added eligible IDs: {eligible_ids} to discount ID: {self.discount_id}")

    def add_buy_items(self, buy_items: List[str]):
        """
        Add buy product IDs to the discount.

        Args:
            buy_items (List[str]): List of product IDs that can be bought to qualify for the discount.
        """
        self.buy_items.update(buy_items)
        logger.debug(f"Added buy items: {buy_items} to discount ID: {self.discount_id}")

    def add_get_items(self, get_items: List[str]):
        """
        Add get product IDs to the discount.

        Args:
            get_items (List[str]): List of product IDs that can be received as part of the discount.
        """
        self.get_items.update(get_items)
        logger.debug(f"Added get items: {get_items} to discount ID: {self.discount_id}")

class DiscountStrategy:
    def __init__(self, strategy_name: str, parameters: Optional[Dict] = None):
        """
        Represents a strategy for applying a discount.

        Args:
            strategy_name (str): Name of the strategy.
            parameters (Dict): Parameters for the strategy.
        """
        self.strategy_name = strategy_name
        self.parameters = parameters or {}

        logger.info(f"Initialized DiscountStrategy: {self.strategy_name} with parameters: {self.parameters}")

    def apply_strategy(self, items: List):
        """
        Apply the strategy to a list of items.

        Args:
            items (List): List of items to apply the strategy on.

        Returns:
            List: Items sorted or filtered based on the strategy.
        """
        logger.debug(f"Applying strategy '{self.strategy_name}' with parameters: {self.parameters}")
        if self.strategy_name == 'lowest_price':
            return sorted(items, key=lambda x: x.product.base_price)
        elif self.strategy_name == 'highest_price':
            return sorted(items, key=lambda x: x.product.base_price, reverse=True)
        # Additional strategies can be added here
        return items

class Promotion:
    def __init__(self, promotion_name: str, discount_ids: List[str], promotion_limit: Optional[int] = None):
        """
        Represents a promotional package containing multiple discounts.

        Args:
            promotion_name (str): Name of the promotion.
            discount_ids (List[str]): List of discount IDs included in the promotion.
            promotion_limit (int): Maximum times the promotion can be applied.
        """
        self.promotion_name = promotion_name
        self.discount_ids = discount_ids
        self.promotion_limit = promotion_limit if promotion_limit is not None else float('inf')
        self.applied_count = 0

        logger.info(f"Initialized Promotion: {self.promotion_name}")

    def apply_promotion(self, cart):
        """
        Apply the promotion to the cart.

        Args:
            cart (Cart): The cart to which the promotion should be applied.

        Returns:
            float: The total discount amount applied by the promotion.
        """
        total_discount = 0.0
        logger.debug(f"Applying promotion '{self.promotion_name}' with discounts: {self.discount_ids}")
        for discount_id in self.discount_ids:
            discount = cart.discounts.get_discount_by_id(discount_id)
            if discount and discount.is_active():
                total_discount += discount.apply_discount(cart)
        self.applied_count += 1
        return total_discount

class DiscountApplicationContext:
    def __init__(self, cart, remaining_limit: int, customer_limit: int):
        """
        Context for applying discounts, holding dynamic data during discount application.

        Args:
            cart (Cart): The cart to which discounts are being applied.
            remaining_limit (int): The remaining limit for the discount.
            customer_limit (int): The limit for discounts specific to the customer.
        """
        self.cart = cart
        self.remaining_limit = remaining_limit
        self.customer_limit = customer_limit
        self.applied_discounts = []

        logger.info(f"Initialized DiscountApplicationContext for cart: {self.cart}")

    def update_limits(self, discount_id: str, limit: int):
        """
        Update the limit for a specific discount.

        Args:
            discount_id (str): The ID of the discount.
            limit (int): The new limit for the discount.
        """
        self.customer_limit[discount_id] = limit
        logger.debug(f"Updated limit for discount ID {discount_id}: {limit}")

    def add_applied_discount(self, discount_id: str):
        """
        Track a discount that has been applied.

        Args:
            discount_id (str): The ID of the discount.
        """
        self.applied_discounts.append(discount_id)
        logger.debug(f"Applied discount ID {discount_id}")

class DiscountLogger:
    def __init__(self, log_level=logging.INFO):
        """
        Logger for discount operations.

        Args:
            log_level (int): Logging level.
        """
        self.logger = logging.getLogger('custom_discounts.core.discount.DiscountLogger')
        self.logger.setLevel(log_level)
        self.log_entries = []

        logger.info("Initialized DiscountLogger")

    def log(self, message: str):
        """
        Log a message.

        Args:
            message (str): Message to log.
        """
        self.logger.info(message)
        self.log_entries.append(message)
        logger.debug(f"Logged message: {message}")

class DiscountValidator:
    def __init__(self, validation_rules: Optional[Dict] = None):
        """
        Validator for checking discount rules and conditions before application.

        Args:
            validation_rules (Dict): Validation rules for discounts.
        """
        self.validation_rules = validation_rules or {}

        logger.info(f"Initialized DiscountValidator with rules: {self.validation_rules}")

    def validate(self, discount: Discount, cart) -> bool:
        """
        Validate if a discount can be applied to the cart.

        Args:
            discount (Discount): The discount to validate.
            cart (Cart): The cart to validate against.

        Returns:
            bool: True if the discount is valid, False otherwise.
        """
        logger.debug(f"Validating discount {discount.discount_id} for cart.")
        if not discount.is_active():
            logger.warning(f"Discount {discount.discount_id} is not active.")
            return False

        # Additional validation logic can be implemented here
        return True
