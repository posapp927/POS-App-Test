# import pandas as pd
# from tabulate import tabulate
#
#
# class Product:
#     def __init__(self, system_id, brand, short_name, size, base_price, category=None, upc=None, qoh=0, pets=None):
#         self.system_id = system_id
#         self.brand = brand
#         self.short_name = short_name
#         self.size = size
#         self.base_price = base_price
#         self.category = category
#         self.upc = upc
#         self.qoh = qoh  # Quantity on Hand
#         self.pets = pets  # Associated pets
#
#     def update_product(self, **kwargs):
#         for key, value in kwargs.items():
#             if hasattr(self, key):
#                 setattr(self, key, value)
#
#
# class ProductCatalog:
#     def __init__(self,
#                  csv_path="database/Cart Table.csv"):
#         self.csv_path = csv_path
#         self.products = {}
#         self.load_products()
#
#     def load_products(self):
#         product_data = pd.read_csv(self.csv_path, dtype={'UPC': str, 'QOH': int})
#         for _, row in product_data.iterrows():
#             product = Product(
#                 system_id=row['System ID'],
#                 brand=row['Brand'],
#                 short_name=row['Short Name'],
#                 size=row['Size'],
#                 base_price=row['Price'],
#                 category=row.get('Category'),
#                 upc=row.get('UPC'),
#                 qoh=row.get('QOH', 0)
#             )
#             self.products[product.system_id] = product
#
#     def get_product(self, system_id):
#         return self.products.get(system_id)
#
#     def add_product(self, system_id, brand, short_name, size, base_price, category=None, upc=None, qoh=0):
#         if system_id in self.products:
#             raise ValueError(f"Product with system ID {system_id} already exists.")
#
#         product = Product(system_id, brand, short_name, size, base_price, category, upc, qoh)
#         self.products[system_id] = product
#
#     def update_product(self, system_id, **kwargs):
#         product = self.get_product(system_id)
#         if product:
#             product.update_product(**kwargs)
#         else:
#             raise ValueError(f"Product with system ID {system_id} not found.")
#
#     def remove_product(self, system_id):
#         if system_id in self.products:
#             del self.products[system_id]
#         else:
#             raise ValueError(f"Product with system ID {system_id} not found.")
#
#     def save_to_csv(self):
#         data = {
#             'System ID': [],
#             'Brand': [],
#             'Short Name': [],
#             'Size': [],
#             'Base Price': [],
#             'Category': [],
#             'UPC': [],
#             'QOH': []
#         }
#
#         for product in self.products.values():
#             data['System ID'].append(product.system_id)
#             data['Brand'].append(product.brand)
#             data['Short Name'].append(product.short_name)
#             data['Size'].append(product.size)
#             data['Base Price'].append(product.base_price)
#             data['Category'].append(product.category)
#             data['UPC'].append(product.upc)
#             data['QOH'].append(product.qoh)
#
#         df = pd.DataFrame(data)
#         df.to_csv(self.csv_path, index=False)
#
#     def get_products_without_categories_or_pets(self):
#         """Return a list of products that have no category or no associated pets."""
#         products_without_categories_or_pets = []
#         for product in self.products.values():
#             if not product.category or not hasattr(product, 'pets') or not product.pets:
#                 product_info = {
#                     'System ID': product.system_id,
#                     'Brand': product.brand,
#                     'Name': product.short_name,
#                     'Size': product.size,
#                     'Category': product.category,
#                     'Pets': product.pets
#                 }
#                 products_without_categories_or_pets.append(product_info)
#
#         # Convert to DataFrame
#         df = pd.DataFrame(products_without_categories_or_pets)
#
#         # Save to CSV
#         file_name = "missing_information.csv"
#         df.to_csv(file_name, index=False)
#
#         # Display the table neatly using tabulate
#         table = tabulate(df, headers='keys', tablefmt='grid')
#         print(table)
#
#         print(f"\nReport generated and saved to {file_name}.")
#
# # Example usage:
# # Initialize the catalog and load products
# # catalog = ProductCatalog()
#
# # # Add a new product
# # catalog.add_product(system_id=100, brand='BrandC', short_name='Product 3', size='S', base_price=10.0, category='CategoryC', upc='123456789012', qoh=50)
#
# # # Update an existing product
# # catalog.update_product(system_id=100, base_price=12.0, qoh=60)
#
# # # Save the updated product data back to the CSV
# # catalog.save_to_csv()
#
#
# # # Initialize the catalog and load products
# # catalog = ProductCatalog()
# #
# # # Get products without categories or pets
# # products_without_categories_or_pets = catalog.get_products_without_categories_or_pets()
# #
# # # Display these products
# # for product in products_without_categories_or_pets:
# #     print(f"System ID: {product.system_id}, Brand: {product.brand}, Name: {product.short_name}, Size: {product.size}, Category: {product.category}, Pets: {product.pets}")
#
#


# class Product:
#     def __init__(self, system_id, brand, short_name, size, base_price, category=None, upc=None, qoh=0, pets=None):
#         self.system_id = system_id
#         self.brand = brand
#         self.short_name = short_name
#         self.size = size
#         self.base_price = base_price
#         self.category = category
#         self.upc = upc
#         self.qoh = qoh  # Quantity on Hand
#         self.pets = pets  # Associated pets
#
#     def update_product(self, **kwargs):
#         for key, value in kwargs.items():
#             if hasattr(self, key):
#                 setattr(self, key, value)
#
#
# class ProductCatalog:
#     def __init__(self, csv_path="database/Cart Table.csv"):
#         self.csv_path = csv_path
#         self.products = {}
#         self.load_products()
#
#     def load_products(self):
#         product_data = pd.read_csv(self.csv_path, dtype={'UPC': str, 'QOH': int})
#         for _, row in product_data.iterrows():
#             product = Product(
#                 system_id=row['System ID'],
#                 brand=row['Brand'],
#                 short_name=row['Short Name'],
#                 size=row['Size'],
#                 base_price=row['Price'],
#                 category=row.get('Category'),
#                 upc=row.get('UPC'),
#                 qoh=row.get('QOH', 0)
#             )
#             self.products[product.system_id] = product
#
#     def get_product(self, system_id):
#         return self.products.get(system_id)
#
#     def add_product(self, system_id, brand, short_name, size, base_price, category=None, upc=None, qoh=0):
#         if system_id in self.products:
#             raise ValueError(f"Product with system ID {system_id} already exists.")
#
#         product = Product(system_id, brand, short_name, size, base_price, category, upc, qoh)
#         self.products[system_id] = product
#
#     def update_product(self, system_id, **kwargs):
#         product = self.get_product(system_id)
#         if product:
#             product.update_product(**kwargs)
#         else:
#             raise ValueError(f"Product with system ID {system_id} not found.")
#
#     def remove_product(self, system_id):
#         if system_id in self.products:
#             del self.products[system_id]
#         else:
#             raise ValueError(f"Product with system ID {system_id} not found.")
#
#     def save_to_csv(self):
#         data = {
#             'System ID': [],
#             'Brand': [],
#             'Short Name': [],
#             'Size': [],
#             'Base Price': [],
#             'Category': [],
#             'UPC': [],
#             'QOH': []
#         }
#
#         for product in self.products.values():
#             data['System ID'].append(product.system_id)
#             data['Brand'].append(product.brand)
#             data['Short Name'].append(product.short_name)
#             data['Size'].append(product.size)
#             data['Base Price'].append(product.base_price)
#             data['Category'].append(product.category)
#             data['UPC'].append(product.upc)
#             data['QOH'].append(product.qoh)
#
#         df = pd.DataFrame(data)
#         df.to_csv(self.csv_path, index=False)
#
#
# class ProductLookup:
#     def __init__(self, product_catalog):
#         self.product_catalog = product_catalog
#         self.product_data = pd.DataFrame([
#             {
#                 'System_ID': str(product.system_id),  # Ensure System ID is treated as a string
#                 'Brand': product.brand,
#                 'Short_Name': product.short_name,
#                 'Size': product.size,
#                 'Base_Price': product.base_price,
#                 'Category': product.category,
#                 'UPC': str(product.upc) if product.upc else None,  # Ensure UPC is treated as a string
#                 'QOH': product.qoh
#             }
#             for product in self.product_catalog.products.values()
#         ])
#
#     def find_product(self, query):
#         query = str(query)
#
#         # Search for the product by UPC or System ID
#         matching_product_upc = self.product_data[self.product_data['UPC'] == query]
#         matching_product_id = self.product_data[self.product_data['System_ID'] == query]
#
#         if not matching_product_upc.empty:
#             product_info = matching_product_upc.replace({np.nan: None}).to_dict(orient='records')[0]
#         elif not matching_product_id.empty:
#             product_info = matching_product_id.replace({np.nan: None}).to_dict(orient='records')[0]
#         else:
#             print('Product not found')
#             return None  # Product not found
#
#         # Return the Product object instead of a dictionary
#         product = self.product_catalog.get_product(int(product_info['System_ID']))
#         return product
#
#     def find_products(self, query):
#         """Find products matching the query in either UPC or System ID."""
#         query = str(query)
#
#         # Filter the products by matching the query in UPC or System ID
#         mask = (self.product_data['UPC'].str.contains(query, na=False)) | \
#                (self.product_data['System_ID'].str.contains(query, na=False))
#
#         matching_products = self.product_data[mask]
#
#         if matching_products.empty:
#             return None  # No products found
#
#         return matching_products.replace({np.nan: None}).to_dict(orient='records')

import pandas as pd
from tabulate import tabulate
import numpy as np

class Product:
    def __init__(self, system_id, brand, name, short_name, size, base_price, category=None, upc=None, qoh=0, pets=None):
        self.system_id = system_id
        self.brand = brand
        self.name = name  # Full product name
        self.short_name = short_name
        self.size = size
        self.base_price = base_price
        self.category = category
        self.upc = upc
        self.qoh = qoh  # Quantity on Hand
        self.pets = pets  # Associated pets

    def update_product(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ProductCatalog:
    def __init__(self, csv_path=None):
        self.csv_path = csv_path
        self.products = {}
        self.load_products()

    def load_products(self):
        product_data = pd.read_csv(self.csv_path, dtype={'UPC': str, 'QOH': int})
        for _, row in product_data.iterrows():
            product = Product(
                system_id=row['System ID'],
                brand=row['Brand'],
                name=row['Name'],  # Load the full product name
                short_name=row['Short Name'],
                size=row['Size'],
                pets=row['Pets'],
                base_price=row['Price'],
                category=row.get('Category'),
                upc=row.get('UPC'),
                qoh=row.get('QOH', 0)
            )
            self.products[product.system_id] = product

    def get_product(self, system_id):
        return self.products.get(system_id)

    def add_product(self, system_id, brand, name, short_name, size, base_price, category=None, upc=None, qoh=0):
        if system_id in self.products:
            raise ValueError(f"Product with system ID {system_id} already exists.")

        product = Product(system_id, brand, name, short_name, size, base_price, category, upc, qoh)
        self.products[system_id] = product

    def update_product(self, system_id, **kwargs):
        product = self.get_product(system_id)
        if product:
            product.update_product(**kwargs)
        else:
            raise ValueError(f"Product with system ID {system_id} not found.")

    def remove_product(self, system_id):
        if system_id in self.products:
            del self.products[system_id]
        else:
            raise ValueError(f"Product with system ID {system_id} not found.")

    def save_to_csv(self):
        data = {
            'System ID': [],
            'Brand': [],
            'Name': [],  # Include full name in the saved data
            'Short Name': [],
            'Size': [],
            'Pets': [],
            'Base Price': [],
            'Category': [],
            'UPC': [],
            'QOH': []
        }

        for product in self.products.values():
            data['System ID'].append(product.system_id)
            data['Brand'].append(product.brand)
            data['Name'].append(product.name)  # Save the full name
            data['Short Name'].append(product.short_name)
            data['Size'].append(product.size)
            data['Pets'].append(product.pets)
            data['Base Price'].append(product.base_price)
            data['Category'].append(product.category)
            data['UPC'].append(product.upc)
            data['QOH'].append(product.qoh)

        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False)



class ProductLookup:
    def __init__(self, product_catalog):
        self.product_catalog = product_catalog
        self.product_data = pd.DataFrame([
            {
                'System_ID': str(product.system_id),  # Ensure System ID is treated as a string
                'Brand': product.brand,
                'Name': product.name,  # Include full name in the lookup
                'Short_Name': product.short_name,
                'Size': product.size,
                'Pets': product.pets,
                'Base_Price': product.base_price,
                'Category': product.category,
                'UPC': str(product.upc) if product.upc else None,  # Ensure UPC is treated as a string
                'QOH': product.qoh
            }
            for product in self.product_catalog.products.values()
        ])

    def find_product(self, query):
        query = str(query)

        # Search for the product by UPC, System ID, or Name
        matching_product_upc = self.product_data[self.product_data['UPC'] == query]
        matching_product_id = self.product_data[self.product_data['System_ID'] == query]
        matching_product_name = self.product_data[self.product_data['Name'].str.contains(query, case=False, na=False)]

        if not matching_product_upc.empty:
            product_info = matching_product_upc.replace({np.nan: None}).to_dict(orient='records')[0]
        elif not matching_product_id.empty:
            product_info = matching_product_id.replace({np.nan: None}).to_dict(orient='records')[0]
        elif not matching_product_name.empty:
            product_info = matching_product_name.replace({np.nan: None}).to_dict(orient='records')[0]
        else:
            print('Product not found')
            return None  # Product not found

        # Return the Product object instead of a dictionary
        product = self.product_catalog.get_product(int(product_info['System_ID']))
        return product

    def find_products(self, query):
        """Find products matching the query in UPC, System ID, or Name."""
        query = str(query)

        # Filter the products by matching the query in UPC, System ID, or Name
        mask = (self.product_data['UPC'].str.contains(query, na=False)) | \
               (self.product_data['System_ID'].str.contains(query, na=False)) | \
               (self.product_data['Name'].str.contains(query, case=False, na=False))

        matching_products = self.product_data[mask]

        if matching_products.empty:
            return None  # No products found

        return matching_products.replace({np.nan: None}).to_dict(orient='records')



