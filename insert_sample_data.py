"""
Script to insert sample data into the database.
"""
from database.db_manager import Database


def insert_member_data(db):
    """Insert sample data into the member table."""
    member_table = db.get_table('member')
    
    members = [
        {
            'member_id': 1,
            'name': 'John Doe',
            'image': 'john.jpg',
            'age': 35,
            'email': 'john.doe@example.com',
            'contact_number': '1234567890'
        },
        {
            'member_id': 2,
            'name': 'Jane Smith',
            'image': 'jane.jpg',
            'age': 28,
            'email': 'jane.smith@example.com',
            'contact_number': '9876543210'
        },
        {
            'member_id': 3,
            'name': 'Bob Johnson',
            'image': 'bob.jpg',
            'age': 42,
            'email': 'bob.johnson@example.com',
            'contact_number': '5551234567'
        }
    ]
    
    for member in members:
        member_table.insert(member)
    
    print(f"Inserted {len(members)} members")


def insert_shop_data(db):
    """Insert sample data into the shop table."""
    shop_table = db.get_table('shop')
    
    shops = [
        {
            'shop_id': 'AB123',
            'name': 'Grocery Store',
            'address': '123 Main St, City',
            'contact': '1112223333',
            'member_id': 1
        },
        {
            'shop_id': 'CD456',
            'name': 'Electronics Shop',
            'address': '456 Oak St, Town',
            'contact': '4445556666',
            'member_id': 2
        },
        {
            'shop_id': 'EF789',
            'name': 'Clothing Boutique',
            'address': '789 Pine St, Village',
            'contact': '7778889999',
            'member_id': 3
        }
    ]
    
    for shop in shops:
        shop_table.insert(shop)
    
    print(f"Inserted {len(shops)} shops")


def insert_customer_data(db):
    """Insert sample data into the customer table."""
    customer_table = db.get_table('customer')
    
    customers = [
        {
            'customer_id': 'RS9876543210',
            'name': 'Alice Brown',
            'contact': '1231231234',
            'email': 'alice.brown@example.com'
        },
        {
            'customer_id': 'RS9876543211',
            'name': 'Charlie Davis',
            'contact': '2342342345',
            'email': 'charlie.davis@example.com'
        },
        {
            'customer_id': 'RS9876543212',
            'name': 'Eve Franklin',
            'contact': '3453453456',
            'email': 'eve.franklin@example.com'
        }
    ]
    
    for customer in customers:
        customer_table.insert(customer)
    
    print(f"Inserted {len(customers)} customers")


def insert_supplier_data(db):
    """Insert sample data into the supplier table."""
    supplier_table = db.get_table('supplier')
    
    suppliers = [
        {
            'supplier_id': 'SYAB12345',
            'name': 'Global Foods',
            'contact': '9998887777',
            'email': 'info@globalfoods.com',
            'address': '100 Supply St, Warehouse District'
        },
        {
            'supplier_id': 'SYCD67890',
            'name': 'Tech Suppliers',
            'contact': '8887776666',
            'email': 'sales@techsuppliers.com',
            'address': '200 Tech Blvd, Industrial Park'
        },
        {
            'supplier_id': 'SYEF13579',
            'name': 'Fashion Wholesale',
            'contact': '7776665555',
            'email': 'orders@fashionwholesale.com',
            'address': '300 Fabric Ave, Fashion District'
        }
    ]
    
    for supplier in suppliers:
        supplier_table.insert(supplier)
    
    print(f"Inserted {len(suppliers)} suppliers")


def insert_product_data(db):
    """Insert sample data into the product table."""
    product_table = db.get_table('product')
    
    products = [
        {
            'product_id': 1,
            'name': 'Apples',
            'category': 'Fruits',
            'supplier_id': 'SYAB12345',
            'shop_id': 'AB123',
            'price': 2.99,
            'stock_quantity': 100,
            'stock_status': 'Normal'
        },
        {
            'product_id': 2,
            'name': 'Laptop',
            'category': 'Electronics',
            'supplier_id': 'SYCD67890',
            'shop_id': 'CD456',
            'price': 999.99,
            'stock_quantity': 10,
            'stock_status': 'Normal'
        },
        {
            'product_id': 3,
            'name': 'T-Shirt',
            'category': 'Clothing',
            'supplier_id': 'SYEF13579',
            'shop_id': 'EF789',
            'price': 19.99,
            'stock_quantity': 50,
            'stock_status': 'Normal'
        },
        {
            'product_id': 4,
            'name': 'Bananas',
            'category': 'Fruits',
            'supplier_id': 'SYAB12345',
            'shop_id': 'AB123',
            'price': 1.99,
            'stock_quantity': 3,
            'stock_status': 'Low Stock'
        }
    ]
    
    for product in products:
        product_table.insert(product)
    
    print(f"Inserted {len(products)} products")


def insert_order_data(db):
    """Insert sample data into the order table."""
    order_table = db.get_table('order')
    
    orders = [
        {
            'order_id': 1,
            'customer_id': 'RS9876543210',
            'shop_id': 'AB123',
            'order_date': '2023-04-01 10:30:00',
            'total_amount': 15.95,
            'status': 'Completed'
        },
        {
            'order_id': 2,
            'customer_id': 'RS9876543211',
            'shop_id': 'CD456',
            'order_date': '2023-04-02 14:45:00',
            'total_amount': 999.99,
            'status': 'Pending'
        },
        {
            'order_id': 3,
            'customer_id': 'RS9876543212',
            'shop_id': 'EF789',
            'order_date': '2023-04-03 16:15:00',
            'total_amount': 59.97,
            'status': 'Completed'
        }
    ]
    
    for order in orders:
        order_table.insert(order)
    
    print(f"Inserted {len(orders)} orders")


def insert_order_details_data(db):
    """Insert sample data into the order_details table."""
    order_details_table = db.get_table('order_details')
    
    order_details = [
        {
            'order_details_id': 1,
            'order_id': 1,
            'product_id': 1,
            'quantity': 5,
            'price': 2.99
        },
        {
            'order_details_id': 2,
            'order_id': 1,
            'product_id': 4,
            'quantity': 1,
            'price': 1.99
        },
        {
            'order_details_id': 3,
            'order_id': 2,
            'product_id': 2,
            'quantity': 1,
            'price': 999.99
        },
        {
            'order_details_id': 4,
            'order_id': 3,
            'product_id': 3,
            'quantity': 3,
            'price': 19.99
        }
    ]
    
    for detail in order_details:
        order_details_table.insert(detail)
    
    print(f"Inserted {len(order_details)} order details")


def main():
    """Insert sample data into the database."""
    # Load the database
    db = Database.load('retail_db')
    
    if db is None:
        print("Database not found. Please run create_tables.py first.")
        return
    
    # Insert sample data
    insert_member_data(db)
    insert_shop_data(db)
    insert_customer_data(db)
    insert_supplier_data(db)
    insert_product_data(db)
    insert_order_data(db)
    insert_order_details_data(db)
    
    # Save the database
    db.save()
    print("Database saved with sample data")


if __name__ == '__main__':
    main()
