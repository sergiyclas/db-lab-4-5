def setup_tables(cursor):
    # Таблиця customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL
        );
    """)

    # Таблиця orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        order_date DATETIME,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

    """)
