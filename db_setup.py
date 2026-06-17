import streamlit as st
import mysql.connector
from mysql.connector import Error

config = st.secrets["mysql"]


def get_connection():
    return mysql.connector.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        ssl_ca=config["ssl_ca"]
    )


def reset_tables(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    cursor.execute("DROP TABLE IF EXISTS sale_items;")
    cursor.execute("DROP TABLE IF EXISTS sales;")
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("DROP TABLE IF EXISTS expenses;")
    cursor.execute("DROP TABLE IF EXISTS staff;")
    cursor.execute("DROP TABLE IF EXISTS suppliers;")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")


def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE suppliers (
            supplier_id INT AUTO_INCREMENT PRIMARY KEY,
            supplier_name VARCHAR(100) NOT NULL,
            contact_person VARCHAR(100),
            phone VARCHAR(30),
            location VARCHAR(100)
        );
    """)

    cursor.execute("""
        CREATE TABLE staff (
            staff_id INT AUTO_INCREMENT PRIMARY KEY,
            staff_name VARCHAR(100) NOT NULL,
            role VARCHAR(50),
            shift VARCHAR(50),
            status VARCHAR(30)
        );
    """)

    cursor.execute("""
        CREATE TABLE products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50),
            supplier_id INT,
            cost_price DECIMAL(10,2),
            selling_price DECIMAL(10,2),
            expiry_date DATE,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE inventory (
            inventory_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            stock_quantity INT NOT NULL,
            reorder_level INT NOT NULL,
            last_updated DATE,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE sales (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            sale_date DATE NOT NULL,
            staff_id INT,
            payment_method VARCHAR(50),
            total_amount DECIMAL(10,2),
            FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE sale_items (
            sale_item_id INT AUTO_INCREMENT PRIMARY KEY,
            sale_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10,2),
            cost_price DECIMAL(10,2),
            total_price DECIMAL(10,2),
            profit DECIMAL(10,2),
            FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE expenses (
            expense_id INT AUTO_INCREMENT PRIMARY KEY,
            expense_date DATE NOT NULL,
            expense_type VARCHAR(100),
            amount DECIMAL(10,2),
            note TEXT
        );
    """)


def insert_sample_data(cursor):
    suppliers = [
        ("Luxe Leather Imports", "Mr Adewale", "08012345678", "Lagos"),
        ("Urban Streetwear Hub", "Mr Malik", "08023456789", "Abuja"),
        ("Premium Footwear Africa", "Mrs Grace", "08034567890", "Ibadan"),
        ("Classic Men Accessories", "Mr Collins", "08045678901", "Port Harcourt")
    ]

    cursor.executemany("""
        INSERT INTO suppliers (supplier_name, contact_person, phone, location)
        VALUES (%s, %s, %s, %s);
    """, suppliers)

    staff = [
        ("Tunde Adebayo", "Sales Associate", "Morning", "Active"),
        ("Daniel Okafor", "Sales Associate", "Evening", "Active"),
        ("Samuel Johnson", "Store Manager", "Morning", "Active"),
        ("Femi Williams", "Inventory Officer", "Evening", "Active")
    ]

    cursor.executemany("""
        INSERT INTO staff (staff_name, role, shift, status)
        VALUES (%s, %s, %s, %s);
    """, staff)

    products = [
        ("Italian Leather Loafers", "Loafers", 1, 32000, 55000, "2028-12-31"),
        ("Black Corporate Oxford", "Corporate Shoes", 1, 28000, 48000, "2028-12-31"),
        ("Urban White Sneakers", "Sneakers", 2, 22000, 38000, "2028-12-31"),
        ("Brown Chelsea Boots", "Boots", 3, 35000, 62000, "2028-12-31"),
        ("OG Premium Slides", "Slides", 2, 9000, 18000, "2028-12-31"),
        ("Luxury Leather Belt", "Belts", 4, 8000, 16000, "2028-12-31"),
        ("Men’s Classic Wallet", "Wallets", 4, 6500, 14000, "2028-12-31"),
        ("Streetwear Baseball Cap", "Caps", 2, 5000, 12000, "2028-12-31"),
        ("Designer Sandals", "Sandals", 3, 15000, 28000, "2028-12-31"),
        ("Premium Polo Shirt", "Apparel", 2, 12000, 25000, "2028-12-31")
    ]

    cursor.executemany("""
        INSERT INTO products 
        (product_name, category, supplier_id, cost_price, selling_price, expiry_date)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, products)

    inventory = [
        (1, 18, 5, "2026-06-09"),
        (2, 15, 5, "2026-06-09"),
        (3, 25, 8, "2026-06-09"),
        (4, 10, 4, "2026-06-09"),
        (5, 30, 10, "2026-06-09"),
        (6, 20, 6, "2026-06-09"),
        (7, 22, 6, "2026-06-09"),
        (8, 35, 10, "2026-06-09"),
        (9, 12, 5, "2026-06-09"),
        (10, 16, 5, "2026-06-09")
    ]

    cursor.executemany("""
        INSERT INTO inventory 
        (product_id, stock_quantity, reorder_level, last_updated)
        VALUES (%s, %s, %s, %s);
    """, inventory)

    sales = [
        ("2026-06-01", 1, "Cash", 55000),
        ("2026-06-02", 2, "POS", 76000),
        ("2026-06-03", 1, "Transfer", 48000),
        ("2026-06-04", 2, "Cash", 62000),
        ("2026-06-05", 1, "POS", 94000),
        ("2026-06-06", 2, "Transfer", 52000),
        ("2026-06-07", 1, "Cash", 80000)
    ]

    cursor.executemany("""
        INSERT INTO sales (sale_date, staff_id, payment_method, total_amount)
        VALUES (%s, %s, %s, %s);
    """, sales)

    sale_items = [
        (1, 1, 1, 55000, 32000, 55000, 23000),

        (2, 3, 2, 38000, 22000, 76000, 32000),

        (3, 2, 1, 48000, 28000, 48000, 20000),

        (4, 4, 1, 62000, 35000, 62000, 27000),

        (5, 1, 1, 55000, 32000, 55000, 23000),
        (5, 6, 1, 16000, 8000, 16000, 8000),
        (5, 7, 1, 14000, 6500, 14000, 7500),
        (5, 8, 1, 12000, 5000, 12000, 7000),

        (6, 9, 1, 28000, 15000, 28000, 13000),
        (6, 5, 1, 18000, 9000, 18000, 9000),
        (6, 8, 1, 12000, 5000, 12000, 7000),

        (7, 10, 2, 25000, 12000, 50000, 26000),
        (7, 6, 1, 16000, 8000, 16000, 8000),
        (7, 7, 1, 14000, 6500, 14000, 7500)
    ]

    cursor.executemany("""
        INSERT INTO sale_items
        (sale_id, product_id, quantity, unit_price, cost_price, total_price, profit)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, sale_items)

    expenses = [
        ("2026-06-01", "Store Rent", 85000, "Monthly boutique rent"),
        ("2026-06-02", "Delivery", 12000, "Logistics for new stock"),
        ("2026-06-03", "Packaging", 18000, "Shopping bags and branded boxes"),
        ("2026-06-05", "Marketing", 25000, "Instagram ads campaign"),
        ("2026-06-07", "Electricity", 10000, "Store power bill")
    ]

    cursor.executemany("""
        INSERT INTO expenses (expense_date, expense_type, amount, note)
        VALUES (%s, %s, %s, %s);
    """, expenses)

    print("OG Urban Kicks sample data inserted successfully.")


def create_indexes(cursor):
    indexes = [
        "CREATE INDEX idx_sales_date ON sales(sale_date);",
        "CREATE INDEX idx_sales_staff ON sales(staff_id);",
        "CREATE INDEX idx_sale_items_sale ON sale_items(sale_id);",
        "CREATE INDEX idx_sale_items_product ON sale_items(product_id);",
        "CREATE INDEX idx_inventory_product ON inventory(product_id);",
        "CREATE INDEX idx_products_supplier ON products(supplier_id);",
        "CREATE INDEX idx_expenses_date ON expenses(expense_date);"
    ]

    for index_query in indexes:
        try:
            cursor.execute(index_query)
        except Error:
            pass


def main():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        reset_tables(cursor)
        create_tables(cursor)
        insert_sample_data(cursor)
        create_indexes(cursor)

        conn.commit()

        print("OG Urban Kicks database setup completed successfully!")

        cursor.close()
        conn.close()

    except Error as e:
        print("Database error:", e)


if __name__ == "__main__":
    main()