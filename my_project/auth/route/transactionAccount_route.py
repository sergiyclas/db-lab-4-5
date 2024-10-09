from flask import request, jsonify
from my_project.auth.service.user_service import TransactionAccountService

transaction_account_service = TransactionAccountService()

def init_transaction_account_routes(app):
    @app.route("/accounts/<int:account_id>/transactions", methods=["GET"])
    def get_transactions_for_account(account_id):
        transactions = transaction_account_service.get_transactions_account_by_id(account_id)
        if not isinstance(transactions, list):
            transactions = [transactions]
        return jsonify([transaction.to_dict() for transaction in transactions])

    @app.route("/accounts/<int:account_id>/transactions", methods=["POST"])
    def link_transaction_to_account(account_id):
        try:
            data = request.get_json()
            transaction_id = data['transaction_id']
            transaction_account_service.create_transactions_account(account_id, transaction_id)
            return jsonify({"message": "Transaction linked successfully"}), 201
        except Exception as e:
            return jsonify(f'Smth went wrong: {e}'), 500

    @app.route("/accounts/transactions", methods=["GET"])
    def show_all_links():
        if request.values:
            account_ids = request.json.get('account_ids')
            transactions = transaction_account_service.get_transactions_account_by_ids(account_ids)

            return jsonify(transactions)

        transactions = transaction_account_service.get_all_transactions_accounts()
        return jsonify([transaction.to_dict() for transaction in transactions])

    @app.route("/accounts/<int:account_id>/transactions", methods=["DELETE"])
    def delete_link_transaction_by_id(account_id):
        transaction_account_service.delete_transactions_account(account_id)
        return jsonify({"message": "Link was deleted successfully"})