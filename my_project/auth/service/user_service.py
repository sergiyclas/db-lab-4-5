# from my_project.auth.dao.user_dao import CustomerDAO, AccountDAO, TransactionDAO, TransactionAccountDAO, PaymentTemplateDAO
from my_project.auth.dao.account_dao import AccountDAO
from my_project.auth.dao.customer_dao import CustomerDAO
from my_project.auth.dao.transaction_dao import TransactionDAO
from my_project.auth.dao.transactionAccount_dao import TransactionAccountDAO
from my_project.auth.dao.paymentTemplate_dao import PaymentTemplateDAO


class CustomerService:
    def __init__(self):
        self.customer_dao = CustomerDAO()

    def get_all_customers(self):
        return self.customer_dao.get_all_customers()

    def get_customer_by_id(self, customer_id):
        return self.customer_dao.get_customer_by_id(customer_id)

    def create_customer(self, customer_name, email, phone):
        return self.customer_dao.create_customer(customer_name, email, phone)

    def update_customer(self, customer_id, customer_name, email, phone):
        self.customer_dao.update_customer(customer_id, customer_name, email, phone)

    def delete_customer(self, customer_id):
        self.customer_dao.delete_customer(customer_id)


class AccountService:
    def __init__(self):
        self.account_dao = AccountDAO()

    def get_all_accounts(self):
        return self.account_dao.get_all_accounts()

    def get_account_by_id(self, account_id):
        return self.account_dao.get_account_by_id(account_id)

    def get_accounts_by_customer_id(self, customer_id):
        return self.account_dao.get_accounts_by_customer_id(customer_id)

    def create_account(self, customer_id, account_number, balance):
        return self.account_dao.create_account(customer_id, account_number, balance)

    def update_account(self, account_id, customer_id, account_number, balance):
        self.account_dao.update_account(account_id, customer_id, account_number, balance)

    def delete_account(self, account_id):
        self.account_dao.delete_account(account_id)


class TransactionService:
    def __init__(self):
        self.transaction_dao = TransactionDAO()

    def get_all_transactions(self):
        return self.transaction_dao.get_all_transactions()

    def get_transaction_by_id(self, transaction_id):
        return self.transaction_dao.get_transaction_by_id(transaction_id)

    def create_transaction(self, amount, transaction_date):
        return self.transaction_dao.create_transaction(amount, transaction_date)

    def update_transaction(self, transaction_id, amount, transaction_date):
        self.transaction_dao.update_transaction(transaction_id, amount, transaction_date)

    def delete_transaction(self, transaction_id):
        self.transaction_dao.delete_transaction(transaction_id)


class TransactionAccountService:
    def __init__(self):
        self.transactions_accounts_dao = TransactionAccountDAO()

    def get_all_transactions_accounts(self):
        return self.transactions_accounts_dao.get_all_transactions_accounts()

    def get_transactions_account_by_id(self, account_id):
        return self.transactions_accounts_dao.get_transactions_account_by_id(account_id)

    def create_transactions_account(self, account_id, transaction_id):
        return self.transactions_accounts_dao.create_transactions_account(account_id, transaction_id)

    def delete_transactions_account(self, id):
        self.transactions_accounts_dao.delete_transactions_account(id)

    def get_transactions_account_by_ids(self, account_ids):
        return self.transactions_accounts_dao.get_transactions_account_by_ids(account_ids)

class PaymentTemplateService:
    def __init__(self):
        self.payment_template_dao = PaymentTemplateDAO()

    def get_all_payment_templates(self):
        return self.payment_template_dao.get_all_payment_templates()

    def get_payment_template_by_id(self, template_id):
        return self.payment_template_dao.get_payment_template_by_id(template_id)

    def create_payment_template(self, account_id, template_name, template_details):
        return self.payment_template_dao.create_payment_template(account_id, template_name, template_details)

    def delete_payment_template(self, template_id):
        self.payment_template_dao.delete_payment_template(template_id)
