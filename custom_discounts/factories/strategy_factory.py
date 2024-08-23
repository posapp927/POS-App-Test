import logging
from typing import Dict, Optional
from custom_discounts.core.discount import DiscountStrategy

logger = logging.getLogger('custom_discounts.factories')

class StrategyFactory:
    def __init__(self):
        """
        Initialize the StrategyFactory with predefined strategies.
        """
        self.predefined_strategies = {
            'lowest_price': self._create_lowest_price_strategy,
            'highest_price': self._create_highest_price_strategy,
            # Additional predefined strategies can be added here
        }
    
    def create_strategy(self, strategy_name: str, parameters: Optional[Dict] = None) -> DiscountStrategy:
        """
        Create a DiscountStrategy based on the given strategy name and parameters.

        Args:
            strategy_name (str): The name of the strategy to create.
            parameters (Dict): Optional parameters for configuring the strategy.

        Returns:
            DiscountStrategy: An instance of the DiscountStrategy class.

        Raises:
            ValueError: If the strategy name is invalid or parameters are missing.
        """
        parameters = parameters or {}
        logger.info(f"Creating strategy '{strategy_name}' with parameters: {parameters}")

        # Check if the strategy is predefined
        if strategy_name in self.predefined_strategies:
            return self.predefined_strategies[strategy_name](parameters)

        # For custom strategies
        return self._create_custom_strategy(strategy_name, parameters)

    def _validate_parameters(self, strategy_name: str, parameters: Dict):
        """
        Validate the parameters for a strategy.

        Args:
            strategy_name (str): The name of the strategy.
            parameters (Dict): The parameters to validate.

        Raises:
            ValueError: If parameters are invalid or missing.
        """
        logger.debug(f"Validating parameters for strategy '{strategy_name}'")
        # Add validation logic based on the strategy name and expected parameters
        if not parameters:
            raise ValueError(f"Parameters are required for strategy '{strategy_name}'")

    def _create_lowest_price_strategy(self, parameters: Dict) -> DiscountStrategy:
        """
        Create a strategy that applies discounts to the lowest priced items first.

        Args:
            parameters (Dict): Parameters for configuring the strategy.

        Returns:
            DiscountStrategy: An instance of the DiscountStrategy class.
        """
        self._validate_parameters('lowest_price', parameters)
        logger.debug("Creating 'lowest_price' strategy")
        return DiscountStrategy(strategy_name='lowest_price', parameters=parameters)

    def _create_highest_price_strategy(self, parameters: Dict) -> DiscountStrategy:
        """
        Create a strategy that applies discounts to the highest priced items first.

        Args:
            parameters (Dict): Parameters for configuring the strategy.

        Returns:
            DiscountStrategy: An instance of the DiscountStrategy class.
        """
        self._validate_parameters('highest_price', parameters)
        logger.debug("Creating 'highest_price' strategy")
        return DiscountStrategy(strategy_name='highest_price', parameters=parameters)

    def _create_custom_strategy(self, strategy_name: str, parameters: Dict) -> DiscountStrategy:
        """
        Create a custom strategy based on user-defined rules.

        Args:
            strategy_name (str): The name of the custom strategy.
            parameters (Dict): Parameters for configuring the custom strategy.

        Returns:
            DiscountStrategy: An instance of the DiscountStrategy class.
        """
        self._validate_parameters(strategy_name, parameters)
        logger.info(f"Creating custom strategy '{strategy_name}' with parameters: {parameters}")
        return DiscountStrategy(strategy_name=strategy_name, parameters=parameters)

    def _register_strategy(self, strategy_name: str, creation_function):
        """
        Register a new strategy dynamically.

        Args:
            strategy_name (str): The name of the strategy.
            creation_function: The function used to create the strategy.
        """
        logger.debug(f"Registering new strategy '{strategy_name}'")
        if strategy_name in self.predefined_strategies:
            raise ValueError(f"Strategy '{strategy_name}' is already registered.")
        self.predefined_strategies[strategy_name] = creation_function

    def _log_creation(self, strategy_name: str, parameters: Dict):
        """
        Log the creation of a strategy.

        Args:
            strategy_name (str): The name of the strategy.
            parameters (Dict): Parameters used to create the strategy.
        """
        logger.info(f"Strategy '{strategy_name}' created with parameters: {parameters}")
