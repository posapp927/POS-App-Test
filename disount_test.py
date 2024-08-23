
import unittest

from Cart import Cart
from Customer import Customer
from Discounts import Discounts
from Product import ProductCatalog, ProductLookup


import unittest

class TestDiscountsIntegration(unittest.TestCase):
    def setUp(self):
        """Set up the test environment with actual classes."""

        self.catalog = ProductCatalog()

        # Initialize the product lookup with the catalog
        self.product_lookup = ProductLookup(self.catalog)
        discounts = Discounts()
        csv_path = "database/bakers_dozen_deal_products.csv"

        # Add the Baker's Dozen discount
        discounts.add_discount(
            discount_id=1,
            discount_type='bakers_dozen',
            details="Baker's Dozen Deal",
            buy_quantity=12,
            get_quantity=1,
            strategy='bakers_dozen'  # Use the newly introduced strategy
        )

        # Load eligible products from CSV and print the loaded products
        discounts.add_eligible_products_from_csv(discount_id=1, csv_path=csv_path)


        # Load additional discounts
        csv_path = 'database/Astro Amount Discount August.csv'
        discounts.add_discounts_from_csv(csv_path)

        # Load customers from CSV and find the customer with ID 6
        customer_list = Customer.load_customers_from_csv('database/POS Customer Data.csv')
        customer = Customer.find_customer_by_id(customer_list, 6)

        # Initialize the cart with the found customer and discounts
        if customer:
            self.cart = Cart(discounts=discounts, customer=customer)
            print(
                f"Initialized cart for Customer ID: {customer.customer_id}, Name: {customer.first_name} {customer.last_name}")
        else:
            raise ValueError("Customer with ID 6 not found.")

    def test_add_item_and_apply_bakers_dozen_discounts(self):
        """Test adding items to the cart and applying Baker's Dozen discount."""
        product1 = self.product_lookup.find_product('073893940012')
        self.assertIsNotNone(product1, "Product lookup returned None. Ensure product data is correctly loaded.")

        for _ in range(13):  # Adding 13 items to trigger 1 free item
            self.cart.add_item(product1)

        # self.cart.add_item(product1, 13)
        # total = self.cart.get_total()
        # self.assertAlmostEqual(total, 2.89 * 12, places=2)  # 12 items paid, 1 item free

        # Test with 26 items, expecting 2 free items in two different clusters
        self.cart.add_item(product1, quantity=13)  # Adding another 13 items
        total = self.cart.get_total()
        self.assertAlmostEqual(total, 2.89 * 24, places=2)  # 24 items paid, 2 items free
        self.cart.get_cart_items()

    def test_mixed_cart_with_bakers_dozen_and_external_discounts(self):
        """Test a mixed cart with various products and the Baker's Dozen and external discounts."""
        product1 = self.product_lookup.find_product('073893940012')
        product2 = self.product_lookup.find_product('811048023193')
        product3 = self.product_lookup.find_product('072705132324')
        product4 = self.product_lookup.find_product('072705132560')
        product5 = self.product_lookup.find_product('810049514747')  # External Discount product
        product6 = self.product_lookup.find_product('691835456539')  # Another External Discount product

        self.assertIsNotNone(product1, "Product 073893940012 not found in catalog.")
        self.assertIsNotNone(product2, "Product 811048023193 not found in catalog.")
        self.assertIsNotNone(product3, "Product 072705132324 not found in catalog.")
        self.assertIsNotNone(product4, "Product 072705132560 not found in catalog.")
        self.assertIsNotNone(product5, "Product 810049514747 not found in catalog.")
        self.assertIsNotNone(product6, "Product 691835456539 not found in catalog.")
        # Add items to test the discount application
        self.cart.add_item(product1, quantity=7)
        self.cart.add_item(product2, quantity=6)
        self.cart.add_item(product3, quantity=4)
        self.cart.add_item(product4, quantity=9)
        self.cart.add_item(product5, quantity=3)
        self.cart.add_item(product6, quantity=5)

        total = self.cart.get_total()
        expected_total = (
            2.89 * 7 +  # Baker's Dozen for product1
            1.79 * 5 +  # Baker's Dozen for product2
            4.19 * 3 +   # No discount for product3
            4.79 * 9 +
            (37.79 * 3 - 5.00 * 3) +  # External discount for product4 (limit 3)
            (38.79 * 5 - 3.00 * 3)    # External discount for product5 (limit 2)
        )
        self.assertAlmostEqual(total, expected_total, places=2)
        self.cart.get_cart_items()

    def test_bakers_dozen_with_mixed_priced_items(self):
        """Test the Baker's Dozen strategy with mixed priced items to ensure the lowest in each cluster is discounted."""
        product1 = self.product_lookup.find_product('073893940012')  # Priced at $2.89
        product2 = self.product_lookup.find_product('811048023193')  # Priced at $1.79

        self.assertIsNotNone(product1, "Product 073893940012 not found in catalog.")
        self.assertIsNotNone(product2, "Product 811048023193 not found in catalog.")

        # Add 26 items, 13 of each product, expecting 1 free of each in each cluster
        self.cart.add_item(product1, quantity=13)
        self.cart.add_item(product2, quantity=13)

        total = self.cart.get_total()
        expected_total = 2.89 * 12 + 1.79 * 12  # Each cluster gives 1 free item, lowest priced in each
        self.assertAlmostEqual(total, expected_total, places=2)
        self.cart.get_cart_items()

    def test_external_discount_limits(self):
        """Test applying external discounts with limits to ensure they don't exceed the limit."""
        product1 = self.product_lookup.find_product('810049514747')  # External Discount product
        product2 = self.product_lookup.find_product('691835456539')  # Another External Discount product

        self.assertIsNotNone(product1, "Product 810049514747 not found in catalog.")
        self.assertIsNotNone(product2, "Product 691835456539 not found in catalog.")

        # Apply external discount to Product 1, which has a limit of 3 applications
        self.cart.add_item(product1, quantity=5)  # Should only apply discount to 3 of these

        # Apply external discount to Product 2, which has a limit of 2 applications
        self.cart.add_item(product2, quantity=3)  # Should only apply discount to 2 of these

        total = self.cart.get_total()
        expected_total = (
            (37.79 * 5 - 5.00 * 3) +  # External discount for product1 (limit 3)
            (38.79 * 3 - 3.00 * 3)    # External discount for product2 (limit 2)
        )
        self.assertAlmostEqual(total, expected_total, places=2)
        self.cart.get_cart_items()






if __name__ == '__main__':
    unittest.main()

