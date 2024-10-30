from my_project.auth.domain.domains import (
    Account
)
from my_project.auth.dao.Base_dao import BaseDAO

class AccountDAO(BaseDAO):
    def get_all_accounts(self):
        self.cursor.execute("SELECT * FROM accounts")
        result = self.cursor.fetchall()
        return [Account(**dict(zip(row, row.values()))) for row in result]

    def get_accounts_by_customer_id(self, customer_id):
        self.cursor.execute("SELECT * FROM accounts WHERE customer_id = %s", (customer_id,))
        result = self.cursor.fetchall()
        return [Account(**row) for row in result]

    def get_account_by_id(self, account_id):
        self.cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (account_id,))
        row = self.cursor.fetchone()
        result = []
        if row:
            return Account(**dict(zip(row, row.values())))
        return result

    def create_account(self, customer_id, account_number, balance):
        self.cursor.execute(
            "INSERT INTO accounts (customer_id, account_number, balance) VALUES (%s, %s, %s)",
            (customer_id, account_number, balance)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def update_account(self, account_id, customer_id, account_number, balance):
        query = "UPDATE accounts SET customer_id = %s, account_number = %s, balance = %s WHERE account_id = %s"
        self.cursor.execute(query, (customer_id, account_number, balance, account_id))
        self.connection.commit()

    def delete_account(self, account_id):
        self.cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
        self.connection.commit()
