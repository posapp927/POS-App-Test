import logging
from typing import Dict, List, Optional
from discount import Discount

# Setup the logger for this module
logger = logging.getLogger('custom_discounts.core.discounts')

class Discounts:
    def __init__(self):
        """
        Initialize the Discounts manager.

        This class manages a collection of Discount instances.
        """
        self.discounts: Dict[str, Discount] = {}
        logger.info("Initialized Discounts manager.")

    def add_discount(self, discount: Discount):
        """
        Add a new discount to the collection.

        Args:
            discount (Discount): The Discount instance to add.
        """
        if discount.discount_id in self.discounts:
            logger.warning(f"Discount with ID {discount.discount_id} already exists. Overwriting.")
        self.discounts[discount.discount_id] = discount
        logger.info(f"Added discount with ID {discount.discount_id}.")

    def get_discount_by_id(self, discount_id: str) -> Optional[Discount]:
        """
        Retrieve a discount by its ID.

        Args:
            discount_id (str): The ID of the discount to retrieve.

        Returns:
            Optional[Discount]: The Discount instance if found, None otherwise.
        """
        return self.discounts.get(discount_id)

    def get_discount_by_name(self, discount_name: str) -> Optional[Discount]:
        """
        Retrieve a discount by its name.

        Args:
            discount_name (str): The name of the discount to retrieve.

        Returns:
            Optional[Discount]: The Discount instance if found, None otherwise.
        """
        for discount in self.discounts.values():
            if discount.details == discount_name:
                return discount
        return None

    def remove_discount(self, discount_id: str) -> bool:
        """
        Remove a discount from the collection.

        Args:
            discount_id (str): The ID of the discount to remove.

        Returns:
            bool: True if the discount was removed, False if it wasn't found.
        """
        if discount_id in self.discounts:
            del self.discounts[discount_id]
            logger.info(f"Removed discount with ID {discount_id}.")
            return True
        logger.warning(f"Attempted to remove non-existent discount with ID {discount_id}.")
        return False

    def apply_discounts(self, cart):
        """
        Apply all applicable discounts to the cart.

        Args:
            cart (Cart): The cart to which discounts should be applied.

        Returns:
            float: The total discount applied.
        """
        total_discount = 0.0
        for discount in self.discounts.values():
            if discount.is_active():
                total_discount += discount.apply_discount(cart)
        logger.info(f"Total discount applied: {total_discount}")
        return total_discount

class DiscountCollection:
    def __init__(self, discounts: Optional[List[Discount]] = None):
        """
        Initialize the DiscountCollection.

        Args:
            discounts (Optional[List[Discount]]): A list of Discount instances to initialize the collection with.
        """
        self.discounts = discounts or []
        logger.info("Initialized DiscountCollection.")

    def add(self, discount: Discount):
        """
        Add a discount to the collection.

        Args:
            discount (Discount): The Discount instance to add.
        """
        self.discounts.append(discount)
        logger.info(f"Added discount with ID {discount.discount_id} to collection.")

    def filter_by_active(self):
        """
        Filter and return only the active discounts.

        Returns:
            List[Discount]: A list of active Discount instances.
        """
        return [discount for discount in self.discounts if discount.is_active()]

    def filter_by_type(self, discount_type: str) -> List[Discount]:
        """
        Filter discounts by their type.

        Args:
            discount_type (str): The type of discounts to filter by.

        Returns:
            List[Discount]: A list of Discount instances matching the type.
        """
        return [discount for discount in self.discounts if discount.discount_type == discount_type]

class DiscountRepository:
    def __init__(self):
        """
        Initialize the DiscountRepository.

        This class serves as an interface for saving and loading discounts from a data source.
        """
        self.storage = {}
        logger.info("Initialized DiscountRepository.")

    def save(self, discount: Discount):
        """
        Save a discount to the repository.

        Args:
            discount (Discount): The Discount instance to save.
        """
        self.storage[discount.discount_id] = discount
        logger.info(f"Saved discount with ID {discount.discount_id} to repository.")

    def load(self, discount_id: str) -> Optional[Discount]:
        """
        Load a discount from the repository.

        Args:
            discount_id (str): The ID of the discount to load.

        Returns:
            Optional[Discount]: The Discount instance if found, None otherwise.
        """
        discount = self.storage.get(discount_id)
        if discount:
            logger.info(f"Loaded discount with ID {discount_id} from repository.")
        else:
            logger.warning(f"Discount with ID {discount_id} not found in repository.")
        return discount
