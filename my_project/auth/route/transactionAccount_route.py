from flask import request, jsonify
from my_project.auth.service.user_service import TransactionAccountService

transaction_account_service = TransactionAccountService()

def init_transaction_account_routes(app):
    @app.route('/transactionaccounts', methods=['GET'])
    def get_transactionaccounts():
        transactionaccounts = transaction_account_service.get_all_transactions_accounts()
        return jsonify(transactionaccounts)

    @app.route("/accounts/<int:account_id>/transactions", methods=["GET"])
    def get_transactions_for_account(account_id):
        transactions = transaction_account_service.get_transactions_account_by_id(account_id)
        return jsonify(transactions)

    @app.route("/accounts/transactions", methods=["POST"])
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
    def show_all_links():
        account_ids = request.get_json().get('account_ids')
        transactions = transaction_account_service.get_transactions_account_by_ids(account_ids)
        return jsonify(transactions)

    @app.route("/accounts/<int:account_id>/transactions", methods=["DELETE"])
    def delete_link_transaction_by_id(account_id):
        transaction_account_service.delete_transactions_account(account_id)
        return jsonify({"message": "Link was deleted successfully"})

    @app.route("/acc/tran", methods=["POST"])
    def create_connection():
        try:
            data = request.get_json()
            value1 = data['value1']
            value2 = data['value2']
            transaction_account_service.create_connection(value1, value2)
            return jsonify({"message": "Transaction linked successfully"}), 201
        except Exception as e:
            return jsonify(f'Something went wrong: {e}'), 500