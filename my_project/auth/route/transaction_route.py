from flask import request, jsonify
from my_project.auth.service.user_service import TransactionService

transaction_service = TransactionService()

def init_transaction_routes(app):
    # Маршрути для транзакцій
    @app.route("/transactions", methods=["GET"])
    def get_transactions():
        transactions = transaction_service.get_all_transactions()
        return jsonify([transaction.to_dict() for transaction in transactions])

    @app.route("/transactions/<int:transaction_id>", methods=["GET"])
    def get_transaction(transaction_id):
        transaction = transaction_service.get_transaction_by_id(transaction_id)
        if transaction:
            return jsonify(transaction.to_dict())
        return jsonify({"error": "Transaction not found"}), 404

    @app.route("/transactions", methods=["POST"])
    def create_transaction():
        data = request.get_json()
        transaction_id = transaction_service.create_transaction(data['amount'], data['transaction_date'])
        return jsonify({"id": transaction_id}), 201

    @app.route("/transactions/<int:transaction_id>", methods=["PUT"])
    def update_transaction(transaction_id):
        data = request.get_json()
        transaction_service.update_transaction(transaction_id, data['amount'], data['transaction_date'])
        return jsonify({"message": "Transaction updated successfully"})

    @app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
    def delete_transaction(transaction_id):
        transaction_service.delete_transaction(transaction_id)
        return jsonify({"message": "Transaction deleted successfully"})
