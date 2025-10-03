import os
import mysql.connector

def load_db_config():
    """Зчитує конфігурацію бази з змінних середовища"""
    return {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))  # дефолт 3306
    }

def connect_to_db():
    db_config = load_db_config()
    connection = mysql.connector.connect(**db_config)
    return connection
