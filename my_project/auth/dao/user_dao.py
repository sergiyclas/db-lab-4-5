import mysql.connector
from my_project.auth.domain.user_domain import User
from config import config

db_config = config.load_db_config()

class UserDAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        return [User(**row) for row in result]

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(**row)
        return None

    def create_user(self, username, email, password):
        self.cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def update_user(self, user_id, username, email, password):
        query = "UPDATE users SET username = %s, email = %s, `password` = %s WHERE id = %s"
        self.cursor.execute(query, (username, email, password, user_id))
        self.connection.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.connection.commit()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()