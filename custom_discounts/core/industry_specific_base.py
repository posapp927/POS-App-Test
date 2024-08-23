import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional, Union

# Setup the logger for this module
logger = logging.getLogger('custom_discounts.core.industry_specific_base')

class IndustrySpecificDiscountBase(ABC):
    def __init__(self, discount_id: str, discount_name: str, eligibility_criteria: Optional[Dict] = None,
                 start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        """
        Base class for industry-specific discounts.

        Args:
            discount_id (str): Unique identifier for the discount.
            discount_name (str): Name of the discount.
            eligibility_criteria (Optional[Dict]): Criteria to determine if the discount applies.
            start_date (Optional[datetime]): Start date of the discount.
            end_date (Optional[datetime]): End date of the discount.
        """
        self.discount_id = discount_id
        self.discount_name = discount_name
        self.eligibility_criteria = eligibility_criteria or {}
        self.start_date = start_date
        self.end_date = end_date
        self.applied_count = 0
        logger.info(f"Initialized industry-specific discount {self.discount_name} with ID {self.discount_id}.")

    @abstractmethod
    def apply_discount(self, cart) -> float:
        """
        Abstract method to apply the discount to a cart.

        Args:
            cart (Cart): The cart to which the discount should be applied.

        Returns:
            float: The total discount applied.
        """
        pass

    def is_active(self) -> bool:
        """
        Check if the discount is currently active based on its start and end dates.

        Returns:
            bool: True if the discount is active, False otherwise.
        """
        now = datetime.now()
        if self.start_date and self.end_date:
            return self.start_date <= now <= self.end_date
        elif self.start_date:
            return self.start_date <= now
        elif self.end_date:
            return now <= self.end_date
        return True

    def validate_criteria(self, cart) -> bool:
        """
        Validate if the cart meets the discount's eligibility criteria.

        Args:
            cart (Cart): The cart to validate against.

        Returns:
            bool: True if the cart meets the criteria, False otherwise.
        """
        # Example logic (can be extended in child classes)
        for key, value in self.eligibility_criteria.items():
            if cart.get_attribute(key) != value:
                logger.info(f"Cart does not meet criteria {key}: expected {value}, found {cart.get_attribute(key)}")
                return False
        return True

    def increment_applied_count(self):
        """
        Increment the count of how many times this discount has been applied.
        """
        self.applied_count += 1
        logger.info(f"Discount {self.discount_name} applied {self.applied_count} times.")

class IndustrySpecificDiscountValidator:
    def __init__(self, validation_rules: Optional[Dict] = None):
        """
        Validator for industry-specific discounts.

        Args:
            validation_rules (Optional[Dict]): Custom validation rules for the discount.
        """
        self.validation_rules = validation_rules or {}
        logger.info("Initialized IndustrySpecificDiscountValidator.")

    def validate(self, discount: IndustrySpecificDiscountBase, cart) -> bool:
        """
        Validate if a discount can be applied to the cart.

        Args:
            discount (IndustrySpecificDiscountBase): The discount to validate.
            cart (Cart): The cart to validate against.

        Returns:
            bool: True if the discount is valid, False otherwise.
        """
        if not discount.is_active():
            logger.info(f"Discount {discount.discount_id} is not active.")
            return False

        if not discount.validate_criteria(cart):
            logger.info(f"Cart does not meet criteria for discount {discount.discount_id}.")
            return False

        logger.info(f"Discount {discount.discount_id} is valid for application.")
        return True

class IndustrySpecificDiscountUpdater:
    def __init__(self, source_url: str, frequency: Optional[str] = 'daily'):
        """
        Handles updating industry-specific discounts from external sources.

        Args:
            source_url (str): The URL to scrape or pull discount data from.
            frequency (Optional[str]): How often to update (e.g., 'daily', 'weekly').
        """
        self.source_url = source_url
        self.frequency = frequency
        self.last_updated = None
        logger.info(f"Initialized IndustrySpecificDiscountUpdater with source {self.source_url}.")

    def fetch_updates(self):
        """
        Fetch updates from the source and update the discounts.

        Returns:
            int: Number of discounts updated.
        """
        logger.info(f"Fetching updates from {self.source_url}.")
        # Implementation of the scraping or API logic goes here
        updated_count = 0
        # After fetching and updating discounts:
        self.last_updated = datetime.now()
        logger.info(f"Updated {updated_count} discounts from {self.source_url}.")
        return updated_count

class IndustrySpecificDiscountManager:
    def __init__(self):
        """
        Manages industry-specific discounts within the system.
        """
        self.discounts: Dict[str, IndustrySpecificDiscountBase] = {}
        self.updater = None
        logger.info("Initialized IndustrySpecificDiscountManager.")

    def add_discount(self, discount: IndustrySpecificDiscountBase):
        """
        Add an industry-specific discount to the system.

        Args:
            discount (IndustrySpecificDiscountBase): The discount to add.
        """
        if discount.discount_id in self.discounts:
            logger.warning(f"Discount with ID {discount.discount_id} already exists. Overwriting.")
        self.discounts[discount.discount_id] = discount
        logger.info(f"Added discount {discount.discount_name} with ID {discount.discount_id}.")

    def apply_discounts(self, cart) -> float:
        """
        Apply all valid industry-specific discounts to the cart.

        Args:
            cart (Cart): The cart to which discounts should be applied.

        Returns:
            float: The total discount applied.
        """
        total_discount = 0.0
        for discount in self.discounts.values():
            validator = IndustrySpecificDiscountValidator()
            if validator.validate(discount, cart):
                total_discount += discount.apply_discount(cart)
        logger.info(f"Total industry-specific discount applied: {total_discount}")
        return total_discount

    def set_updater(self, updater: IndustrySpecificDiscountUpdater):
        """
        Set the updater instance for fetching discount updates.

        Args:
            updater (IndustrySpecificDiscountUpdater): The updater instance.
        """
        self.updater = updater
        logger.info("Set the discount updater.")

    def update_discounts(self):
        """
        Update the discounts using the updater.
        """
        if self.updater:
            updated_count = self.updater.fetch_updates()
            logger.info(f"Updated {updated_count} discounts.")
        else:
            logger.warning("No updater set for IndustrySpecificDiscountManager.")
