import logging
from custom_discounts.core.discount import Discount

logger = logging.getLogger('custom_discounts.factories')

class DiscountFactory:
    def create_discount(self, discount_type, **kwargs):
        """
        Create a Discount object based on the provided discount type and parameters.

        Args:
            discount_type (str): The type of discount to create.
            **kwargs: Additional parameters required to create the discount.

        Returns:
            Discount: An instance of the Discount class or its subclasses.
        """
        self._validate_parameters(discount_type, kwargs)
        
        if discount_type == 'percentage':
            return self._create_percentage_discount(**kwargs)
        elif discount_type == 'fixed_amount':
            return self._create_fixed_amount_discount(**kwargs)
        elif discount_type == 'buy_x_get_y_free':
            return self._create_buy_get_free_discount(**kwargs)
        elif discount_type == 'custom':
            return self._create_custom_discount(**kwargs)
        else:
            logger.error(f"Unsupported discount type: {discount_type}")
            raise ValueError(f"Unsupported discount type: {discount_type}")

    def _validate_parameters(self, discount_type, params):
        """
        Validate parameters for the discount creation.

        Args:
            discount_type (str): The type of discount being created.
            params (dict): The parameters provided for discount creation.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        # Example validation: Ensure required fields are present
        required_fields = ['amount', 'discount_id', 'details']
        missing_fields = [field for field in required_fields if field not in params]
        
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Additional validation logic can be added here
        logger.debug(f"Parameters validated for discount type: {discount_type}")

    def _create_percentage_discount(self, **kwargs):
        """
        Create a percentage-based discount.

        Returns:
            Discount: The percentage-based Discount object.
        """
        logger.info("Creating a percentage-based discount.")
        return Discount(discount_type='percentage', **kwargs)

    def _create_fixed_amount_discount(self, **kwargs):
        """
        Create a fixed amount discount.

        Returns:
            Discount: The fixed amount Discount object.
        """
        logger.info("Creating a fixed amount discount.")
        return Discount(discount_type='fixed_amount', **kwargs)

    def _create_buy_get_free_discount(self, **kwargs):
        """
        Create a buy_x_get_y_free discount.

        Returns:
            Discount: The buy_x_get_y_free Discount object.
        """
        logger.info("Creating a buy_x_get_y_free discount.")
        return Discount(discount_type='buy_x_get_y_free', **kwargs)

    def _create_custom_discount(self, **kwargs):
        """
        Create a custom discount based on user-defined parameters.

        Returns:
            Discount: The custom Discount object.
        """
        logger.info("Creating a custom discount.")
        return Discount(discount_type='custom', **kwargs)
