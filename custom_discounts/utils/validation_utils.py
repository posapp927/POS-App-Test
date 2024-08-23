# custom_discounts/utils/validation_utils.py

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

class ValidationError(Exception):
    """Custom exception raised when validation fails."""
    pass

class Validator:
    """
    A utility class for validating various data inputs, configurations, and rules within the discount system.
    """

    @staticmethod
    def validate_type(value: Any, expected_type: type, field_name: str) -> None:
        """Ensure the value is of the expected type."""
        if not isinstance(value, expected_type):
            raise ValidationError(f"Invalid type for '{field_name}'. Expected {expected_type.__name__}, got {type(value).__name__}.")

    @staticmethod
    def validate_range(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float], field_name: str) -> None:
        """Ensure the value is within the specified range."""
        if not (min_value <= value <= max_value):
            raise ValidationError(f"Invalid value for '{field_name}'. Expected between {min_value} and {max_value}, got {value}.")

    @staticmethod
    def validate_format(value: str, pattern: str, field_name: str) -> None:
        """Ensure the value matches the specified regex pattern."""
        if not re.match(pattern, value):
            raise ValidationError(f"Invalid format for '{field_name}'. Value '{value}' does not match the expected format.")

    @staticmethod
    def validate_length(value: str, min_length: int, max_length: int, field_name: str) -> None:
        """Ensure the string value's length is within the specified bounds."""
        if not (min_length <= len(value) <= max_length):
            raise ValidationError(f"Invalid length for '{field_name}'. Expected between {min_length} and {max_length} characters, got {len(value)} characters.")

    @staticmethod
    def validate_not_empty(value: Any, field_name: str) -> None:
        """Ensure the value is not empty."""
        if value is None or (isinstance(value, (str, list, dict)) and not value):
            raise ValidationError(f"The field '{field_name}' cannot be empty.")

    @staticmethod
    def validate_lifetime(lifetime: Union[str, List[str]]) -> Union[datetime, Tuple[datetime, datetime]]:
        """Validate and parse the lifetime into datetime objects."""
        if isinstance(lifetime, str):
            return Validator._parse_date(lifetime)
        elif isinstance(lifetime, list) and len(lifetime) == 2:
            return (Validator._parse_date(lifetime[0]), Validator._parse_date(lifetime[1]))
        else:
            raise ValidationError(f"Invalid lifetime format: {lifetime}")

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse a date string into a datetime object."""
        try:
            return datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            raise ValidationError(f"Invalid date format: '{date_str}'. Expected 'MM/DD/YYYY'.")

    @staticmethod
    def validate_discount_configuration(discount_config: Dict[str, Any]) -> None:
        """Validate a discount configuration dictionary."""
        # Required fields
        required_fields = ['discount_id', 'discount_name', 'amount']
        for field in required_fields:
            Validator.validate_not_empty(discount_config.get(field), field)

        # Type checks
        Validator.validate_type(discount_config['discount_id'], str, 'discount_id')
        Validator.validate_type(discount_config['discount_name'], str, 'discount_name')
        Validator.validate_type(discount_config['amount'], (int, float), 'amount')

        # Range checks (example: ensuring percentage-based discounts are within 0-100)
        if 'discount_type' in discount_config and discount_config['discount_type'] == 'percentage':
            Validator.validate_range(discount_config['amount'], 0, 100, 'amount')

        # Validate lifetime if present
        if 'lifetime' in discount_config:
            Validator.validate_lifetime(discount_config['lifetime'])

    @staticmethod
    def validate_promotion_configuration(promotion_config: Dict[str, Any], existing_discount_ids: List[str]) -> None:
        """Validate a promotion configuration dictionary."""
        # Required fields
        required_fields = ['promotion_name', 'discount_ids']
        for field in required_fields:
            Validator.validate_not_empty(promotion_config.get(field), field)

        # Type checks
        Validator.validate_type(promotion_config['promotion_name'], str, 'promotion_name')
        Validator.validate_type(promotion_config['discount_ids'], list, 'discount_ids')

        # Ensure all discount IDs are valid
        for discount_id in promotion_config['discount_ids']:
            if discount_id not in existing_discount_ids:
                raise ValidationError(f"Invalid discount_id '{discount_id}' in promotion configuration. It does not exist in the system.")

    @staticmethod
    def validate_strategy_configuration(strategy_config: Dict[str, Any], valid_strategies: List[str]) -> None:
        """Validate a strategy configuration dictionary."""
        # Required fields
        required_fields = ['strategy_name']
        for field in required_fields:
            Validator.validate_not_empty(strategy_config.get(field), field)

        # Type checks
        Validator.validate_type(strategy_config['strategy_name'], str, 'strategy_name')

        # Ensure strategy name is valid
        if strategy_config['strategy_name'] not in valid_strategies:
            raise ValidationError(f"Invalid strategy_name '{strategy_config['strategy_name']}'. Expected one of {valid_strategies}.")

    @staticmethod
    def validate_unique_ids(id_list: List[str], entity_name: str) -> None:
        """Ensure that all IDs in the list are unique."""
        if len(id_list) != len(set(id_list)):
            raise ValidationError(f"Duplicate IDs found in {entity_name}. IDs must be unique.")

    @staticmethod
    def validate_cross_promotion_rules(discount_configs: List[Dict[str, Any]]) -> None:
        """Ensure that no conflicting rules exist across multiple discounts."""
        # Example: Ensure that no two 'fixed_amount' discounts apply to the same item
        for i, discount in enumerate(discount_configs):
            for other_discount in discount_configs[i+1:]:
                if discount['discount_type'] == 'fixed_amount' and other_discount['discount_type'] == 'fixed_amount':
                    if set(discount.get('eligible_ids', [])) & set(other_discount.get('eligible_ids', [])):
                        raise ValidationError(f"Conflicting discounts found: '{discount['discount_id']}' and '{other_discount['discount_id']}' apply fixed amounts to the same items.")

    @staticmethod
    def validate_tax_compliance(discount_config: Dict[str, Any], tax_region: str) -> None:
        """Ensure the discount complies with tax regulations."""
        # Example: Ensure that taxable discounts are correctly marked
        if discount_config.get('discount_taxable') and tax_region not in discount_config.get('applicable_regions', []):
            raise ValidationError(f"Discount '{discount_config['discount_id']}' is marked as taxable but is not compliant with tax regulations in the '{tax_region}' region.")

    @staticmethod
    def validate_promotion_overlap(promotion_configs: List[Dict[str, Any]]) -> None:
        """Ensure promotions do not overlap in a way that violates business rules."""
        # Example: Validate that promotions do not apply the same discount multiple times
        discount_usage = {}
        for promotion in promotion_configs:
            for discount_id in promotion['discount_ids']:
                discount_usage[discount_id] = discount_usage.get(discount_id, 0) + 1
                if discount_usage[discount_id] > 1:
                    raise ValidationError(f"Discount '{discount_id}' is applied in multiple promotions which may violate business rules.")

    @staticmethod
    def log_validation_errors(errors: List[str]) -> None:
        """Log validation errors for auditing purposes."""
        for error in errors:
            # Assume there's a logger set up already
            logging.error(f"Validation error: {error}")
