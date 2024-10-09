from my_project.auth.domain.domains import (
    Transaction
)
from my_project.auth.dao.Base_dao import BaseDAO

class TransactionDAO(BaseDAO):
    def get_all_transactions(self):
        self.cursor.execute("SELECT * FROM transactions")
        result = self.cursor.fetchall()
        return [Transaction(**row) for row in result]

    def get_transaction_by_id(self, transaction_id):
        self.cursor.execute("SELECT * FROM transactions WHERE transaction_id = %s", (transaction_id,))
        row = self.cursor.fetchone()
        if row:
            return Transaction(**row)
        return None

    def create_transaction(self, amount, transaction_date):
        self.cursor.execute(
            "INSERT INTO transactions (amount, transaction_date) VALUES (%s, %s)",
            (amount, transaction_date)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def update_transaction(self, transaction_id, amount, transaction_date):
        query = "UPDATE transactions SET amount = %s, transaction_date = %s WHERE transaction_id = %s"
        self.cursor.execute(query, (amount, transaction_date, transaction_id))
        self.connection.commit()

    def delete_transaction(self, transaction_id):
        self.cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", (transaction_id,))
        self.connection.commit()