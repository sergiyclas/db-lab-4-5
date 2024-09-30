import mysql.connector
from my_project.auth.domain.domains import (
    Customer, Account, Transaction, TransactionsAccounts, PaymentTemplate,
    Card, Need, Authorization, Fee, StatusTransaction
)
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


class CustomerDAO(BaseDAO):
    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM customers")
        result = self.cursor.fetchall()
        return [Customer(**row) for row in result]

    def get_customer_by_id(self, customer_id):
        self.cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        row = self.cursor.fetchone()
        if row:
            return Customer(**row)
        return None

    def create_customer(self, customer_name, email, phone):
        self.cursor.execute(
            "INSERT INTO customers (customer_name, email, phone) VALUES (%s, %s, %s)",
            (customer_name, email, phone)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def update_customer(self, customer_id, customer_name, email, phone):
        query = "UPDATE customers SET customer_name = %s, email = %s, phone = %s WHERE customer_id = %s"
        self.cursor.execute(query, (customer_name, email, phone, customer_id))
        self.connection.commit()

    def delete_customer(self, customer_id):
        self.cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        self.connection.commit()


class AccountDAO(BaseDAO):
    def get_all_accounts(self):
        self.cursor.execute("SELECT * FROM accounts")
        result = self.cursor.fetchall()
        return [Account(**row) for row in result]

    def get_account_by_id(self, account_id):
        self.cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (account_id,))
        row = self.cursor.fetchone()
        if row:
            return Account(**row)
        return None

    def create_account(self, customer_id, account_number, balance):
        self.cursor.execute(
            "INSERT INTO accounts (customer_id, account_number, balance) VALUES (%s, %s, %s)",
            (customer_id, account_number, balance)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def update_account(self, account_id, account_number, balance):
        query = "UPDATE accounts SET account_number = %s, balance = %s WHERE account_id = %s"
        self.cursor.execute(query, (account_number, balance, account_id))
        self.connection.commit()

    def delete_account(self, account_id):
        self.cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
        self.connection.commit()


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


class TransactionsAccountsDAO(BaseDAO):
    def get_all_transactions_accounts(self):
        self.cursor.execute("SELECT * FROM TransactionsAccounts")
        result = self.cursor.fetchall()
        return [TransactionsAccounts(**row) for row in result]

    def get_transactions_account_by_id(self, id):
        self.cursor.execute("SELECT * FROM TransactionsAccounts WHERE id = %s", (id,))
        row = self.cursor.fetchone()
        if row:
            return TransactionsAccounts(**row)
        return None

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


class PaymentTemplateDAO(BaseDAO):
    def get_all_payment_templates(self):
        self.cursor.execute("SELECT * FROM payment_templates")
        result = self.cursor.fetchall()
        return [PaymentTemplate(**row) for row in result]

    def get_payment_template_by_id(self, template_id):
        self.cursor.execute("SELECT * FROM payment_templates WHERE template_id = %s", (template_id,))
        row = self.cursor.fetchone()
        if row:
            return PaymentTemplate(**row)
        return None

    def create_payment_template(self, account_id, template_name, template_details):
        self.cursor.execute(
            "INSERT INTO payment_templates (account_id, template_name, template_details) VALUES (%s, %s, %s)",
            (account_id, template_name, template_details)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def delete_payment_template(self, template_id):
        self.cursor.execute("DELETE FROM payment_templates WHERE template_id = %s", (template_id,))
        self.connection.commit()


# class UserDAO:
#     def __init__(self):
#         self.connection = mysql.connector.connect(
#             host=db_config['host'],
#             user=db_config['user'],
#             password=db_config['password'],
#             database=db_config['database']
#         )
#         self.cursor = self.connection.cursor(dictionary=True)
#
#     def get_all_users(self):
#         self.cursor.execute("SELECT * FROM users")
#         result = self.cursor.fetchall()
#         return [User(**row) for row in result]
#
#     def get_user_by_id(self, user_id):
#         self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#         row = self.cursor.fetchone()
#         if row:
#             return User(**row)
#         return None
#
#     def create_user(self, username, email, password):
#         self.cursor.execute(
#             "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password)
#         )
#         self.connection.commit()
#         return self.cursor.lastrowid
#
#     def update_user(self, user_id, username, email, password):
#         query = "UPDATE users SET username = %s, email = %s, `password` = %s WHERE id = %s"
#         self.cursor.execute(query, (username, email, password, user_id))
#         self.connection.commit()
#
#     def delete_user(self, user_id):
#         self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#         self.connection.commit()
#
#     def __del__(self):
#         if self.cursor is not None:
#             self.cursor.close()
#         if self.connection is not None:
#             self.connection.close()