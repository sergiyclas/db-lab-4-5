import mysql.connector
from config import config

db_config = config.load_db_config()


class BaseDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
