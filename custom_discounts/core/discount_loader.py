import csv
import logging
import uuid
from typing import Dict, List, Optional
from discount import Discount
from discounts import Discounts

# Setup the logger for this module
logger = logging.getLogger('custom_discounts.core.discount_loader')

class DiscountLoader:
    def __init__(self, discounts: Discounts):
        """
        Initialize the DiscountLoader.

        Args:
            discounts (Discounts): Instance of the Discounts class to manage discounts.
        """
        self.discounts = discounts
        self.column_mapping = {}
        logger.info("Initialized DiscountLoader.")

    def _auto_map_columns(self, header: List[str]) -> Dict[str, str]:
        """
        Automatically maps CSV columns to Discount attributes based on header names.

        Args:
            header (List[str]): List of column headers from the CSV file.

        Returns:
            Dict[str, str]: Mapping of CSV columns to Discount attributes.
        """
        attribute_map = {
            'discount_id': 'discount_id',
            'discount name': 'details',
            'discount type': 'discount_type',
            'buy quantity': 'buy_quantity',
            'get quantity': 'get_quantity',
            'amount': 'amount',
            'strategy': 'strategy',
            'strategy limit': 'strategy_limit',
            'lifetime': 'lifetime',
            'limit': 'limit',
            'discount taxable': 'discount_taxable',
        }

        mapped_columns = {}
        for column in header:
            normalized_column = column.strip().replace('_', ' ').lower()
            for key, value in attribute_map.items():
                if key.replace('_', ' ') == normalized_column:
                    mapped_columns[value] = column
                    break

        logger.debug(f"Automatically mapped columns: {mapped_columns}")
        return mapped_columns

    def _prompt_for_missing_columns(self, header: List[str], auto_mapped_columns: Dict[str, str]) -> Dict[str, str]:
        """
        Prompts the user to map any missing columns.

        Args:
            header (List[str]): List of column headers from the CSV file.
            auto_mapped_columns (Dict[str, str]): Automatically mapped columns.

        Returns:
            Dict[str, str]: Final mapping of CSV columns to Discount attributes.
        """
        required_attributes = {'details'}  # Only 'details' (discount name) is required, others are optional
        missing_attributes = required_attributes - set(auto_mapped_columns.keys())

        for attribute in missing_attributes:
            print(f"Please map the column for '{attribute}':")
            print(f"Available columns: {header}")
            selected_column = input(f"Enter the column name for '{attribute}': ").strip()
            auto_mapped_columns[attribute] = selected_column

        logger.info(f"User-mapped columns: {auto_mapped_columns}")
        return auto_mapped_columns

    def _generate_discount_id(self) -> str:
        """Generate a unique discount ID."""
        return str(uuid.uuid4())

    def load_discounts_from_csv(self, file_path: str) -> None:
        """
        Loads discounts from a CSV file.

        Args:
            file_path (str): Path to the CSV file.

        Raises:
            ValueError: If the required discount details (name) are not provided.
        """
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames

            if not header:
                logger.error("CSV file has no headers.")
                raise ValueError("CSV file has no headers.")

            # Attempt to auto-map columns based on the header
            auto_mapped_columns = self._auto_map_columns(header)

            # Prompt user for missing mappings
            column_mapping = self._prompt_for_missing_columns(header, auto_mapped_columns)

            # Load the discounts using the final column mapping
            for row in reader:
                discount_data = {}
                for attr, col in column_mapping.items():
                    discount_data[attr] = row.get(col, None)

                # Ensure discount details (name) is provided
                if not discount_data.get('details'):
                    logger.error("Discount name is required but not provided in the CSV.")
                    raise ValueError("Discount name is required but not provided in the CSV.")

                # Check if a discount with the same name already exists
                existing_discount = self.discounts.get_discount_by_name(discount_data['details'])
                
                if existing_discount:
                    logger.info(f"Found existing discount with name '{discount_data['details']}'. Appending data.")
                    # Append data to the existing discount (you may need to define how this append works)
                    self._append_to_existing_discount(existing_discount, discount_data)
                else:
                    # Generate a discount ID if not provided
                    if not discount_data.get('discount_id'):
                        discount_data['discount_id'] = self._generate_discount_id()
                        logger.info(f"Generated discount ID {discount_data['discount_id']} for '{discount_data['details']}'")

                    # Convert fields to appropriate data types
                    discount = Discount(
                        discount_id=discount_data['discount_id'],
                        discount_type=discount_data.get('discount_type'),
                        details=discount_data.get('details'),
                        buy_quantity=int(discount_data.get('buy_quantity', 0)),
                        get_quantity=int(discount_data.get('get_quantity', 0)),
                        amount=float(discount_data.get('amount', 0.0)),
                        strategy=discount_data.get('strategy'),
                        strategy_limit=int(discount_data.get('strategy_limit', 0)) if discount_data.get('strategy_limit') else None,
                        lifetime=discount_data.get('lifetime'),
                        limit=int(discount_data.get('limit', 0)) if discount_data.get('limit') else None,
                        discount_taxable=discount_data.get('discount_taxable', 'True').lower() == 'true'
                    )

                    # Add the discount to the Discounts collection
                    self.discounts.add_discount(discount)
                    logger.info(f"Added new discount: {discount}")

    def _append_to_existing_discount(self, existing_discount: Discount, discount_data: Dict[str, str]) -> None:
        """
        Appends data to an existing discount.

        Args:
            existing_discount (Discount): The existing Discount instance.
            discount_data (Dict[str, str]): The new data to append.
        """
        # Example of appending logic, this should be expanded based on your needs
        if discount_data.get('buy_quantity'):
            existing_discount.buy_quantity = int(discount_data.get('buy_quantity'))
        if discount_data.get('get_quantity'):
            existing_discount.get_quantity = int(discount_data.get('get_quantity'))
        if discount_data.get('amount'):
            existing_discount.amount = float(discount_data.get('amount'))
        # Add more fields as necessary
        logger.info(f"Appended data to existing discount {existing_discount.discount_id}")
