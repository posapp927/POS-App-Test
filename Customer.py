import pandas as pd


class Customer:
    def __init__(self, customer_id, first_name, last_name, email=None, phone=None, total_transaction=0):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.total_transaction = total_transaction
        self.applied_discounts = {}  # Track applied discounts per discount ID

    def get_applied_discount_count(self, discount_id):
        """Retrieve the count of how many times a discount has been applied for this customer."""
        return self.applied_discounts.get(discount_id, 0)

    def increment_applied_discount_count(self, discount_id, count):
        """Increment the count of applied discounts for this customer."""
        if discount_id not in self.applied_discounts:
            self.applied_discounts[discount_id] = 0
        self.applied_discounts[discount_id] += count

    @staticmethod
    def load_customers_from_csv(csv_path):
        """Load customers from a CSV file and return a list of Customer instances."""
        customer_df = pd.read_csv(csv_path, dtype={'Phone': str, 'Total Transaction': float})

        customers = []
        for _, row in customer_df.iterrows():
            customer = Customer(
                customer_id=row['ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                email=row.get('Email', None),
                phone=row.get('Phone', None),
                total_transaction=row.get('Total Transaction', 0)
            )
            customers.append(customer)
        return customers

    @staticmethod
    def search_customers(customers, query):
        """Search customers by ID, name, email, or phone."""
        query = query.lower()
        matches = []
        for customer in customers:
            # Handle potential NaN values for phone, first_name, last_name, and email
            phone_str = customer.phone if pd.notna(customer.phone) else ''
            first_name = customer.first_name if pd.notna(customer.first_name) else ''
            last_name = customer.last_name if pd.notna(customer.last_name) else ''
            email = customer.email if pd.notna(customer.email) else ''

            if (query in str(customer.customer_id).lower() or
                    query in first_name.lower() or
                    query in last_name.lower() or
                    query in email.lower() or
                    query in str(phone_str).lower()):
                matches.append(customer)

        for match in matches:
            print(match.first_name, match.last_name, match.email, match.phone)
        return matches

    @staticmethod
    def get_customer_by_id(customers, customer_id):
        """Find a customer by their ID."""
        return next((customer for customer in customers if customer.customer_id == customer_id), None)


    # @staticmethod
    # def find_customer_by_id(customers, customer_id):
    #     """Find a customer by their ID."""
    #     for customer in customers:
    #         if customer.customer_id == customer_id:
    #             return customer
    #     return None
