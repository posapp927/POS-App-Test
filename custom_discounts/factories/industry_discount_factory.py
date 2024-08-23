import logging
from typing import Dict, Optional
from custom_discounts.astro_discounts.astro_discount import AstroDiscount
from custom_discounts.core.industry_specific_base import IndustrySpecificDiscountBase

logger = logging.getLogger('custom_discounts.factories')

class IndustryDiscountFactory:
    def __init__(self):
        """
        Initialize the IndustryDiscountFactory with predefined discount types.
        """
        self.predefined_discount_types = {
            'astro': self._create_astro_discount,
            # Additional industry-specific discounts can be added here
        }
    
    def create_discount(self, discount_type: str, parameters: Optional[Dict] = None) -> IndustrySpecificDiscountBase:
        """
        Create an industry-specific discount based on the given type and parameters.

        Args:
            discount_type (str): The type of the discount to create (e.g., 'astro').
            parameters (Dict): Optional parameters for configuring the discount.

        Returns:
            IndustrySpecificDiscountBase: An instance of the industry-specific discount class.

        Raises:
            ValueError: If the discount type is invalid or parameters are missing.
        """
        parameters = parameters or {}
        logger.info(f"Creating industry-specific discount of type '{discount_type}' with parameters: {parameters}")

        # Check if the discount type is predefined
        if discount_type in self.predefined_discount_types:
            return self.predefined_discount_types[discount_type](parameters)

        # For custom or unregistered discount types
        raise ValueError(f"Unknown discount type '{discount_type}'")

    def _validate_parameters(self, discount_type: str, parameters: Dict):
        """
        Validate the parameters for an industry-specific discount.

        Args:
            discount_type (str): The type of the discount.
            parameters (Dict): The parameters to validate.

        Raises:
            ValueError: If parameters are invalid or missing.
        """
        logger.debug(f"Validating parameters for industry-specific discount '{discount_type}'")
        # Add validation logic based on the discount type and expected parameters
        if not parameters:
            raise ValueError(f"Parameters are required for industry-specific discount '{discount_type}'")

    def _create_astro_discount(self, parameters: Dict) -> AstroDiscount:
        """
        Create an AstroDiscount based on the given parameters.

        Args:
            parameters (Dict): Parameters for configuring the AstroDiscount.

        Returns:
            AstroDiscount: An instance of the AstroDiscount class.
        """
        self._validate_parameters('astro', parameters)
        logger.debug("Creating 'AstroDiscount' with parameters")
        return AstroDiscount(**parameters)

    def _register_discount_type(self, discount_type: str, creation_function):
        """
        Register a new industry-specific discount type dynamically.

        Args:
            discount_type (str): The name of the discount type.
            creation_function: The function used to create the discount.

        Raises:
            ValueError: If the discount type is already registered.
        """
        logger.debug(f"Registering new industry-specific discount type '{discount_type}'")
        if discount_type in self.predefined_discount_types:
            raise ValueError(f"Discount type '{discount_type}' is already registered.")
        self.predefined_discount_types[discount_type] = creation_function

    def _log_creation(self, discount_type: str, parameters: Dict):
        """
        Log the creation of an industry-specific discount.

        Args:
            discount_type (str): The type of the discount.
            parameters (Dict): Parameters used to create the discount.
        """
        logger.info(f"Industry-specific discount '{discount_type}' created with parameters: {parameters}")
