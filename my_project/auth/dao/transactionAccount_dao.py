from my_project.auth.domain.domains import (
    Transaction, TransactionsAccounts, Transaction_All_Info
)
from my_project.auth.dao.Base_dao import BaseDAO

class TransactionAccountDAO(BaseDAO):
    def get_all_transactions_accounts(self):
        self.cursor.execute("SELECT * FROM TransactionsAccounts")
        result = self.cursor.fetchall()
        return [TransactionsAccounts(**row) for row in result]

    def get_transactions_account_by_ids(self, account_ids):
        if not account_ids:
            self.cursor.execute("SELECT account_id FROM accounts")
            result = self.cursor.fetchall()
            account_ids = [account['account_id'] for account in result]

        format_strings = ','.join(['%s'] * len(account_ids))
        query = f"""
            SELECT 
                ta1.account_id AS source_account_id,
                a1.account_number AS source_account_number,
                ta2.account_id AS destination_account_id,
                a2.account_number AS destination_account_number,
                t.transaction_id,
                t.amount,

                f.fee_amount,

                s.status,
                s.status_date
            FROM 
                TransactionsAccounts ta1
            JOIN 
                TransactionsAccounts ta2 ON ta1.transaction_id = ta2.transaction_id AND ta1.account_id != ta2.account_id
            JOIN 
                accounts a1 ON ta1.account_id = a1.account_id
            JOIN 
                accounts a2 ON ta2.account_id = a2.account_id
            JOIN 
                transactions t ON ta1.transaction_id = t.transaction_id
            LEFT JOIN 
                fees f ON t.transaction_id = f.transaction_id
            LEFT JOIN 
                status_transactions s ON t.transaction_id = s.transaction_id
            WHERE 
                a1.account_id IN ({format_strings}) OR a2.account_id IN ({format_strings})
            ORDER BY 
                t.transaction_date, t.transaction_id
        """

        # Execute the query with `account_ids` as parameters twice (for both source and destination filters)
        self.cursor.execute(query, account_ids + account_ids)

        result = self.cursor.fetchall()
        transactions = {}
        for row in result:
            transaction_data = dict(zip(row, row.values()))

            transaction = {
                "transaction_id": transaction_data['transaction_id'],
                "amount": transaction_data['amount'],
                # "transaction_date": transaction_data['transaction_date'],
                "fee_amount": transaction_data['fee_amount'],
                # "fee_date": transaction_data['fee_date'],
                "status": transaction_data['status'],
                "status_date": transaction_data['status_date'],
                "source_account_id": transaction_data['source_account_id'],
                "source_account_number": transaction_data['source_account_number'],
                # "source_account_balance": transaction_data['source_account_balance'],
                "destination_account_id": transaction_data['destination_account_id'],
                "destination_account_number": transaction_data['destination_account_number'],
                # "destination_account_balance": transaction_data['destination_account_balance'],
            }

            # Group transactions by source account
            if not f"account_{transaction_data['source_account_id']}" in transactions:
                transactions[f"account_{transaction_data['source_account_id']}"] = [transaction]
            else:
                transactions[f"account_{transaction_data['source_account_id']}"].append(transaction)

        return transactions

    def get_transactions_account_by_id(self, account_id):
        self.cursor.execute("""
            SELECT t.transaction_id, t.amount, t.transaction_date, f.fee_amount, f.fee_date, s.status, s.status_date 
            FROM transactions t
            JOIN TransactionsAccounts ta ON t.transaction_id = ta.transaction_id
            LEFT JOIN fees f ON t.transaction_id = f.transaction_id
            LEFT JOIN status_transactions s ON t.transaction_id = s.transaction_id
            WHERE ta.account_id = %s
        """, (account_id,))

        result = self.cursor.fetchall()

        transactions = []
        for row in result:
            transaction_data = dict(zip(row, row.values()))

            transaction = Transaction_All_Info(
                transaction_id=transaction_data['transaction_id'],
                amount=transaction_data['amount'],
                transaction_date=transaction_data['transaction_date'],
                fee_amount=transaction_data['fee_amount'],
                fee_date=transaction_data['fee_date'],
                status=transaction_data['status'],
                status_date=transaction_data['status_date']
            )
            transactions.append(transaction)

        return transactions

    def create_transactions_account(self, account_id, transaction_id):
        self.cursor.execute(
            "INSERT INTO TransactionsAccounts (account_id, transaction_id) VALUES (%s, %s)",
            (account_id, transaction_id)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def delete_transactions_account(self, id):
        self.cursor.execute("DELETE FROM TransactionsAccounts WHERE id = %s", (id,))
        self.connection.commit()

    def create_connection(self, value1, value2):
        self.cursor.execute(
            "CALL insert_into_relation_accounts_transactions(%s, %s)",
            (value1, value2)
        )
        self.connection.commit()
        return self.cursor.lastrowid
