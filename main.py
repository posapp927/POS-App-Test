import pandas as pd
from flask import Flask, render_template, jsonify, request

from Cart import Cart
from Customer import Customer
from Discounts import Discounts
from Product import ProductCatalog, ProductLookup
import os

app = Flask(__name__)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the CSV file
product_catalog_path = os.path.join(current_dir, "database", "Cart Table.csv")

product_catalog = ProductCatalog(product_catalog_path)
product_lookup = ProductLookup(product_catalog)


discounts = Discounts()

bakers_dozen_discount_path = os.path.join(current_dir, "database", "bakers_dozen_deal_products.csv")
# Add the Baker's Dozen discount
discounts.add_discount(
    discount_id=1,
    discount_type='bakers_dozen',
    details="Baker's Dozen Deal",
    buy_quantity=12,
    get_quantity=1,
    strategy='bakers_dozen'
)

# Load eligible products from CSV and print the loaded products
discounts.add_eligible_products_from_csv(discount_id=1, csv_path=bakers_dozen_discount_path)


astro_amount_discount_path = os.path.join(current_dir, "database", "Astro Amount Discount August.csv")
discounts.add_discounts_from_csv(astro_amount_discount_path)

astro_buyxgety_discount_path = os.path.join(current_dir, "database", "Astro Buy X Get Y Free August 2024.csv")
discounts.add_discounts_from_csv(astro_buyxgety_discount_path)

customer_data_path = os.path.join(current_dir, "database", "POS Customer Data.csv")
# Load customers from CSV and find the customer with ID 6
customer_list = Customer.load_customers_from_csv(customer_data_path)
# customer = Customer.get_customer_by_id(customer_list, 6)
# Initialize the cart with discounts but no customer yet
cart = Cart(discounts=discounts)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/manage-inventory')
def manage_inventory():
    return render_template('manage-inventory.html')

@app.route('/to_index')
def to_index():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search_product():
    query = request.args.get('query', '').strip()
    if len(query) > 3:
        # Use the find_products method from the ProductLookup class
        results = product_lookup.find_products(query)
        if results:
            return jsonify(results)
    return jsonify([])  # Return an empty list if no results or query is too short


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    system_id = data.get('system_id')

    # Attempt to find the product
    product = product_lookup.find_product(system_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found.'}), 404

    # Add product to the cart
    cart.add_item(product)

    # Get cart items and prepare data for response
    cart_items = cart.get_cart_items()
    cart_data = [format_cart_item(cart_item) for cart_item in cart_items]

    # Print the cart data for debugging purposes
    print('cart_data', cart_data)

    # Return the cart data as a JSON response
    return jsonify({'success': True, 'cart': cart_data})

def format_cart_item(cart_item):
    """
    Helper function to format a single cart item for the response.

    Args:
        cart_item (dict): The cart item data from get_cart_items().

    Returns:
        dict: The formatted cart item data for the response.
    """
    discount_id = cart_item.get('discount_id', None)
    discount_name = ""

    if discount_id:
        discount_data = cart.discounts.get_discount_by_id(discount_id)
        if discount_data:
            discount_name = discount_data['details']

    return {
            'cart_id': cart_item.get('cart_id') or '',  # Ensure cart_id is a string, default to an empty string
            'product_name': cart_item.get('product_name', '') or '',  # Default to an empty string if None
            'brand': cart_item.get('brand', '') or '',  # Default to an empty string if None
            'size': cart_item.get('size', '') or '',  # Default to an empty string if None
            'pets': cart_item.get('pets', '') or '',  # Default to an empty string if None
            'quantity': cart_item.get('quantity', 0) or 0,  # Default to 0 if None
            'base_price': cart_item.get('base_price', 0.0) or 0.0,  # Default to 0.0 if None
            'discounted_quantity': cart_item.get('discounted_quantity', 0) or 0,  # Default to 0 if None
            'non_discounted_quantity': cart_item.get('non_discounted_quantity', 0) or 0,  # Default to 0 if None
            'discount_amount': cart_item.get('discount_amount', 0.0) or 0.0,  # Default to 0.0 if None
            'regular_total_price': cart_item.get('regular_total_price', 0.0) or 0.0,  # Default to 0.0 if None
            'discounted_total_price': cart_item.get('discounted_total_price', 0.0) or 0.0,  # Default to 0.0 if None
            'total_price': cart_item.get('total_price', 0.0) or 0.0,  # Default to 0.0 if None
            'discount_name': discount_name or '',  # Ensure discount_name is a string, default to an empty string
            'discount_id': discount_id or '',  # Ensure discount_id is a string, default to an empty string
            'discount_taxable': cart_item.get('discount_amount', 0.0) > 0,  # Default to False if discount_amount is 0 or None
            'system_id': cart_item.get('system_id', '') or '',  # Default to an empty string if None
            'upc': cart_item.get('upc', '') or '',  # Default to an empty string if None
            'sub_cart_items': cart_item.get('sub_cart_items', '') or ''
        }



@app.route('/search_customer', methods=['GET'])
def search_customer():
    query = request.args.get('query', '').strip()
    if len(query) > 3:
        matching_customers = Customer.search_customers(customer_list, query)  # Assume customer_list is loaded

        results = []
        for customer in matching_customers:
            phone_formatted = format_phone_number(customer.phone) if pd.notna(customer.phone) else ''
            contact_info = f"{phone_formatted}"
            if customer.email and pd.notna(customer.email):
                contact_info += f" | {customer.email}"

            results.append({
                'customer_id': customer.customer_id,
                'name': f"{customer.first_name if pd.notna(customer.first_name) else ''} {customer.last_name if pd.notna(customer.last_name) else ''}",
                'contact_info': contact_info.strip(' | ')  # Remove trailing separator if only one contact detail
            })

        return jsonify(results)

    return jsonify([])  # Return empty list if query is too short


def format_phone_number(phone):
    """Format phone number as (XXX) XXX-XXXX."""
    phone = ''.join(filter(str.isdigit, str(phone)))  # Remove any non-numeric characters
    if len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    return phone  # Return as is if it's not 10 digits


@app.route('/add_customer_to_cart', methods=['POST'])
def add_customer_to_cart():
    data = request.get_json()
    customer_id = data.get('customer_id')

    # Validate that a customer_id is provided
    if not customer_id:
        return jsonify({'success': False, 'message': 'Customer ID is required.'}), 400

    # Find the customer by ID
    customer = Customer.get_customer_by_id(customer_list, customer_id)
    if not customer:
        return jsonify({'success': False, 'message': 'Customer not found.'}), 404

    # Set the customer to the cart
    cart.set_customer(customer)  # Assume `cart` is an instance of Cart

    return jsonify({'success': True, 'message': f'Customer {customer.first_name} {customer.last_name} added to cart.'})




if __name__ == '__main__':
    app.run(debug=True)






