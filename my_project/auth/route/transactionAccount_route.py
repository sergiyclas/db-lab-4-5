from flask import request, jsonify
from my_project.auth.service.user_service import TransactionAccountService
from flasgger import swag_from

transaction_account_service = TransactionAccountService()

def init_transaction_account_routes(app):
    @app.route('/transactionaccounts', methods=['GET'])
    @swag_from({
        'tags': ['TransactionAccounts'],
        'summary': 'Get all transaction-account links',
        'description': 'Retrieve all transaction-account link records from the system.',
        'responses': {
            200: {
                'description': 'List of all transaction-account links',
                'content': {
                    'application/json': {
                        'example': [
                            {"account_id": 1, "transaction_id": 2},
                            {"account_id": 3, "transaction_id": 5}
                        ]
                    }
                }
            }
        }
    })
    def get_transactionaccounts():
        transactionaccounts = transaction_account_service.get_all_transactions_accounts()
        return jsonify(transactionaccounts)

    @app.route("/accounts/<int:account_id>/transactions", methods=["GET"])
    @swag_from({
        'tags': ['TransactionAccounts'],
        'summary': 'Get transactions for an account',
        'description': 'Retrieve all transactions linked to a specific account by account ID.',
        'parameters': [
            {
                'name': 'account_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the account',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Transactions linked to the account',
                'content': {
                    'application/json': {
                        'example': [
                            {"transaction_id": 2, "amount": 150.75, "transaction_date": "2024-01-10"}
                        ]
                    }
                }
            }
        }
    })
    def get_transactions_for_account(account_id):
        transactions = transaction_account_service.get_transactions_account_by_id(account_id)
        return jsonify(transactions)

    @app.route("/accounts/transactions", methods=["POST"])
    @swag_from({
        'tags': ['TransactionAccounts'],
        'summary': 'Link a transaction to an account',
        'description': 'Create a link between a transaction and an account by providing their IDs.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"account_id": 1, "transaction_id": 2}
                }
            }
        },
        'responses': {
            201: {
                'description': 'Transaction successfully linked',
                'content': {
                    'application/json': {'example': {"message": "Transaction linked successfully"}}
                }
            },
            500: {'description': 'Server error'}
        }
    })
    def link_transaction_to_account():
        try:
            data = request.get_json()
            account_id = data['account_id']
            transaction_id = data['transaction_id']
            transaction_account_service.create_transactions_account(account_id, transaction_id)
            return jsonify({"message": "Transaction linked successfully"}), 201
        except Exception as e:
            return jsonify(f'Something went wrong: {e}'), 500

    @app.route("/accounts/transactions", methods=["GET"])
    @swag_from({
        'tags': ['TransactionAccounts'],
        'summary': 'Show all links for multiple accounts',
        'description': 'Retrieve transactions linked to multiple account IDs.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"account_ids": [1, 2, 3]}
                }
            }
        },
        'responses': {
            200: {
                'description': 'Transactions linked to the provided accounts',
                'content': {
                    'application/json': {
                        'example': [
                            {"account_id": 1, "transaction_id": 2},
                            {"account_id": 2, "transaction_id": 1}
                        ]
                    }
                }
            }
        }
    })
    def show_all_links():
        account_ids = request.get_json().get('account_ids')
        transactions = transaction_account_service.get_transactions_account_by_ids(account_ids)
        return jsonify(transactions)

    @app.route("/accounts/<int:account_id>/transactions", methods=["DELETE"])
    @swag_from({
        'tags': ['TransactionAccounts'],
        'summary': 'Delete transaction links for an account',
        'description': 'Delete all transaction links for a specific account by account ID.',
        'parameters': [
            {
                'name': 'account_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the account',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Links successfully deleted',
                'content': {
                    'application/json': {'example': {"message": "Link was deleted successfully"}}
                }
            }
        }
    })
    def delete_link_transaction_by_id(account_id):
        transaction_account_service.delete_transactions_account(account_id)
        return jsonify({"message": "Link was deleted successfully"})

    @app.route("/acc/tran", methods=["POST"])
    @swag_from({
        'tags': ['TransactionAccounts'],
        'summary': 'Create connection between two values',
        'description': 'Create a transaction link using two arbitrary values (value1, value2).',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"value1": 1, "value2": 2}
                }
            }
        },
        'responses': {
            201: {
                'description': 'Connection successfully created',
                'content': {
                    'application/json': {'example': {"message": "Transaction linked successfully"}}
                }
            },
            500: {'description': 'Server error'}
        }
    })
    def create_connection():
        try:
            data = request.get_json()
            value1 = data['value1']
            value2 = data['value2']
            transaction_account_service.create_connection(value1, value2)
            return jsonify({"message": "Transaction linked successfully"}), 201
        except Exception as e:
            return jsonify(f'Something went wrong: {e}'), 500
