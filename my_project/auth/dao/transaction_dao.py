from my_project.auth.domain.domains import (
    Transaction, Log, Result
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

    def get_all_logs(self):
        query = 'SELECT * FROM logs'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [Log(**row) for row in result]

    def get_log_by_transaction_id(self, transaction_id):
        self.cursor.execute("SELECT * FROM logs WHERE transaction_id = %s", (transaction_id,))
        result = self.cursor.fetchall()
        if result:
            return [Log(**row) for row in result]
        return None

    def insert_into_table(self, table_name, column_list, value_list):
        query = rf"""CALL insert_into_table('{table_name}', '{column_list}', "{value_list}");"""
        # print(query)
        # self.cursor.execute(query)
        # self.connection.commit()
        return None

    def count_transaction(self, column_name, operation):
        self.cursor.execute(
            "CALL select_with_function_transactions (%s, %s)",
            (column_name, operation)
        )
        res = self.cursor.fetchall()
        self.connection.close()
        if res:
            return [Result(**row) for row in res]
        return None

    def create_tables(self):
        self.cursor.execute("CALL CreateRandomTransactionTablesAndCopyData()")
        self.connection.commit()