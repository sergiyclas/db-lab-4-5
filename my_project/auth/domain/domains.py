from datetime import datetime
from typing import Optional

# Клас для таблиці customers
class Customer:
    def __init__(self, customer_id: int, customer_name: str, email: Optional[str], phone: Optional[str]):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "email": self.email,
            "phone": self.phone
        }

# Клас для таблиці accounts
class Account:
    def __init__(self, account_id: int, customer_id: int, account_number: str, balance: float):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = balance

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "account_number": self.account_number,
            "balance": self.balance
        }

# Клас для таблиці transactions
class Transaction:
    def __init__(self, transaction_id, amount, transaction_date):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_date = transaction_date

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_date": self.transaction_date,
        }

class Log:
    def __init__(self, log_id, transaction_id, log_action, log_time):
        self.log_id = log_id
        self.transaction_id = transaction_id
        self.log_action = log_action
        self.log_time = log_time

    def to_dict(self):
        return {
            "log_id": self.log_id,
            "transaction_id": self.transaction_id,
            "log_action": self.log_action,
            "log_time": self.log_time,
        }

class Result:
    def __init__(self, result):
        self.result = result

    def to_dict(self):
        return {
            "result": self.result
        }

# Клас для таблиці transactions
class Transaction_All_Info:
    def __init__(self, transaction_id, amount, transaction_date, fee_amount=None, fee_date=None, status=None, status_date=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_date = transaction_date
        self.fee_amount = fee_amount
        self.fee_date = fee_date
        self.status = status
        self.status_date = status_date

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_date": self.transaction_date,
            "fee_amount": self.fee_amount,
            "fee_date": self.fee_date,
            "status": self.status,
            "status_date": self.status_date
        }

# Клас для таблиці TransactionsAccounts
class TransactionsAccounts:
    def __init__(self, id: int, account_id: int, transaction_id: int):
        self.id = id
        self.account_id = account_id
        self.transaction_id = transaction_id

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "transaction_id": self.transaction_id
        }

# Клас для таблиці payment_templates
class PaymentTemplate:
    def __init__(self, template_id: int, account_id: int, template_name: str, template_details: Optional[str]):
        self.template_id = template_id
        self.account_id = account_id
        self.template_name = template_name
        self.template_details = template_details

    def to_dict(self):
        return {
            "template_id": self.template_id,
            "account_id": self.account_id,
            "template_name": self.template_name,
            "template_details": self.template_details
        }

# Клас для таблиці cards
class Card:
    def __init__(self, card_id: int, account_id: int, card_number: str, card_type: Optional[str], expiry_date: Optional[datetime]):
        self.card_id = card_id
        self.account_id = account_id
        self.card_number = card_number
        self.card_type = card_type
        self.expiry_date = expiry_date

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "account_id": self.account_id,
            "card_number": self.card_number,
            "card_type": self.card_type,
            "expiry_date": self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None
        }

# Клас для таблиці needs
class Need:
    def __init__(self, need_id: int, transaction_id: int, service_name: str, payment_date: Optional[datetime], description: Optional[str], category: Optional[str], priority: Optional[int]):
        self.need_id = need_id
        self.transaction_id = transaction_id
        self.service_name = service_name
        self.payment_date = payment_date
        self.description = description
        self.category = category
        self.priority = priority

    def to_dict(self):
        return {
            "need_id": self.need_id,
            "transaction_id": self.transaction_id,
            "service_name": self.service_name,
            "payment_date": self.payment_date.strftime('%Y-%m-%d') if self.payment_date else None,
            "description": self.description,
            "category": self.category,
            "priority": self.priority
        }

# Клас для таблиці authorizations
class Authorization:
    def __init__(self, auth_id: int, account_id: int, login_time: Optional[datetime], logout_time: Optional[datetime], password: str):
        self.auth_id = auth_id
        self.account_id = account_id
        self.login_time = login_time
        self.logout_time = logout_time
        self.password = password

    def to_dict(self):
        return {
            "auth_id": self.auth_id,
            "account_id": self.account_id,
            "login_time": self.login_time.strftime('%Y-%m-%d %H:%M:%S') if self.login_time else None,
            "logout_time": self.logout_time.strftime('%Y-%m-%d %H:%M:%S') if self.logout_time else None,
            "password": self.password
        }

# Клас для таблиці fees
class Fee:
    def __init__(self, fee_id: int, transaction_id: int, fee_amount: float, fee_date: Optional[datetime]):
        self.fee_id = fee_id
        self.transaction_id = transaction_id
        self.fee_amount = fee_amount
        self.fee_date = fee_date

    def to_dict(self):
        return {
            "fee_id": self.fee_id,
            "transaction_id": self.transaction_id,
            "fee_amount": self.fee_amount,
            "fee_date": self.fee_date.strftime('%Y-%m-%d') if self.fee_date else None
        }

# Клас для таблиці status_transactions
class StatusTransaction:
    def __init__(self, status_id: int, transaction_id: int, status: str, status_date: Optional[datetime]):
        self.status_id = status_id
        self.transaction_id = transaction_id
        self.status = status
        self.status_date = status_date

    def to_dict(self):
        return {
            "status_id": self.status_id,
            "transaction_id": self.transaction_id,
            "status": self.status,
            "status_date": self.status_date.strftime('%Y-%m-%d') if self.status_date else None
        }
