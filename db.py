import mysql.connector
from mysql.connector import Error
from config import config
import os

config = config.load_db_config()

def create_database_if_not_exists(config):
    """Створення бази даних, якщо вона не існує, без підключення до конкретної БД."""
    config_without_db = config.copy()
    config_without_db.pop("database", None)
    connection = mysql.connector.connect(**config_without_db)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS online_banking")
    print("База даних створена або вже існує.")
    cursor.close()
    connection.close()

def execute_sql_file(connection, sql_file_path):
    """Виконання SQL-файлу для створення таблиць та заповнення даних."""
    cursor = connection.cursor()
    if not os.path.exists(sql_file_path):
        print(f"Файл {sql_file_path} не знайдено!")
        return
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_commands = f.read().split(';')  # Розбиваємо на окремі команди
        for command in sql_commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"Помилка виконання команди:\n{command}\n{e}")
    connection.commit()
    cursor.close()
    print(f"SQL-файл {sql_file_path} виконано успішно!")

def main():
    # Створюємо базу даних, якщо не існує
    create_database_if_not_exists(config)

    # Підключаємося до БД
    config['database'] = 'online_banking'
    connection = mysql.connector.connect(**config)

    # Виконуємо SQL-файл
    execute_sql_file(connection, "scenary.sql")

    # Закриваємо підключення
    connection.close()

if __name__ == "__main__":
    main()
