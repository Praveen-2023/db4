"""
Script to create database tables from the SQL schema.
"""
import os
from database.db_manager import Database


def create_member_table(db):
    """Create the member table."""
    schema = {
        'member_id': 'int',
        'name': 'str',
        'image': 'str',
        'age': 'int',
        'email': 'str',
        'contact_number': 'str'
    }
    db.create_table('member', schema, 'member_id')
    print("Created member table")


def create_shop_table(db):
    """Create the shop table."""
    schema = {
        'shop_id': 'str',
        'name': 'str',
        'address': 'str',
        'contact': 'str',
        'member_id': 'int'
    }
    db.create_table('shop', schema, 'shop_id')
    print("Created shop table")


def create_customer_table(db):
    """Create the customer table."""
    schema = {
        'customer_id': 'str',
        'name': 'str',
        'contact': 'str',
        'email': 'str'
    }
    db.create_table('customer', schema, 'customer_id')
    print("Created customer table")


def create_supplier_table(db):
    """Create the supplier table."""
    schema = {
        'supplier_id': 'str',
        'name': 'str',
        'contact': 'str',
        'email': 'str',
        'address': 'str'
    }
    db.create_table('supplier', schema, 'supplier_id')
    print("Created supplier table")


def create_product_table(db):
    """Create the product table."""
    schema = {
        'product_id': 'int',
        'name': 'str',
        'category': 'str',
        'supplier_id': 'str',
        'shop_id': 'str',
        'price': 'float',
        'stock_quantity': 'int',
        'stock_status': 'str'
    }
    db.create_table('product', schema, 'product_id')
    print("Created product table")


def create_order_table(db):
    """Create the order table."""
    schema = {
        'order_id': 'int',
        'customer_id': 'str',
        'shop_id': 'str',
        'order_date': 'str',
        'total_amount': 'float',
        'status': 'str'
    }
    db.create_table('order', schema, 'order_id')
    print("Created order table")


def create_order_details_table(db):
    """Create the order_details table."""
    schema = {
        'order_details_id': 'int',
        'order_id': 'int',
        'product_id': 'int',
        'quantity': 'int',
        'price': 'float'
    }
    db.create_table('order_details', schema, 'order_details_id')
    print("Created order_details table")


def create_employee_table(db):
    """Create the employee table."""
    schema = {
        'employee_id': 'int',
        'name': 'str',
        'role': 'str',
        'contact': 'str',
        'shop_id': 'str',
        'salary': 'float',
        'salary_status': 'str'
    }
    db.create_table('employee', schema, 'employee_id')
    print("Created employee table")


def create_payment_table(db):
    """Create the payment table."""
    schema = {
        'payment_id': 'int',
        'order_id': 'int',
        'amount': 'float',
        'method': 'str',
        'transaction_timestamp': 'str'
    }
    db.create_table('payment', schema, 'payment_id')
    print("Created payment table")


def create_attendance_table(db):
    """Create the attendance table."""
    schema = {
        'employee_id': 'int',
        'attendance_date': 'str',
        'check_in': 'str',
        'check_out': 'str',
        'status': 'str'
    }
    db.create_table('attendance', schema, 'employee_id')
    print("Created attendance table")


def create_loyalty_table(db):
    """Create the loyalty table."""
    schema = {
        'loyalty_id': 'int',
        'customer_id': 'str',
        'shop_id': 'str',
        'purchase_amount': 'float',
        'loyalty_points': 'int',
        'purchase_date': 'str',
        'points_valid_till': 'str'
    }
    db.create_table('loyalty', schema, 'loyalty_id')
    print("Created loyalty table")


def main():
    """Create the database and tables."""
    # Create the data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Create the database
    db = Database('retail_db')
    
    # Create the tables
    create_member_table(db)
    create_shop_table(db)
    create_customer_table(db)
    create_supplier_table(db)
    create_product_table(db)
    create_order_table(db)
    create_order_details_table(db)
    create_employee_table(db)
    create_payment_table(db)
    create_attendance_table(db)
    create_loyalty_table(db)
    
    # Save the database
    db.save()
    print("Database saved")


if __name__ == '__main__':
    main()
