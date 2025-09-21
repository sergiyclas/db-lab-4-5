import mysql.connector
from mysql.connector import Error
from config import config

config = config.load_db_config()

def create_database():
    config_without_db = config.copy()
    config_without_db.pop("database")  # прибираємо 'database'
    connection = mysql.connector.connect(**config_without_db)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS online_banking")
    connection.commit()
    cursor.close()
    connection.close()


def create_connection():
    """Створення підключення до MySQL."""
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Підключення до MySQL успішне!")
    except Error as e:
        print(f"Помилка підключення до MySQL: {e}")
    return connection

def create_database(connection):
    """Створення бази даних, якщо вона не існує."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS db_lab_4_5")
    print("База даних створена або вже існує.")
    cursor.close()

def create_tables(connection):
    """Створення таблиць users та інші, якщо вони не існують."""
    tables = {
        "users": """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        # Можеш додати інші таблиці тут, наприклад, для products або orders
    }

    cursor = connection.cursor()
    for table_name, table_sql in tables.items():
        try:
            cursor.execute(table_sql)
            print(f"Таблиця {table_name} створена або вже існує.")
        except Error as e:
            print(f"Помилка створення таблиці {table_name}: {e}")
    cursor.close()

def insert_sample_data(connection):
    """Вставка тестових даних у таблиці, якщо вони ще не існують."""
    cursor = connection.cursor()
    # Перевірка наявності записів
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        # Якщо таблиця порожня, вставляємо тестові дані
        insert_user_query = """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """
        users_data = [
            ('admin', 'admin@example.com', 'adminpassword'),
            ('user1', 'user1@example.com', 'password1'),
            ('user2', 'user2@example.com', 'password2')
        ]
        cursor.executemany(insert_user_query, users_data)
        connection.commit()
        print("Тестові дані додані в таблицю users.")
    else:
        print("Дані вже існують у таблиці users.")
    cursor.close()

def main():
    # Створюємо підключення до MySQL
    create_database()

    # connection = create_connection()

    # if connection is not None and connection.is_connected():
        # Створюємо базу даних (якщо ще не створена)
        # create_database(connection)

    # Перепідключаємося до новоствореної БД
    # config['database'] = 'db_lab_4_5'
    connection = mysql.connector.connect(**config)

    # Створюємо таблиці
    create_tables(connection)

    # Вставляємо тестові дані
    insert_sample_data(connection)

    # Закриваємо з'єднання
    connection.close()

if __name__ == "__main__":
    main()
