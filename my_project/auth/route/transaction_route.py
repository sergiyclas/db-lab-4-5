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

    @app.route("/logs", methods=["GET"])
    def get_logs():
        logs = transaction_service.get_all_logs()
        return jsonify([log.to_dict() for log in logs])

    @app.route("/logs/<int:transaction_id>/transactions", methods=["GET"])
    def get_logs_by_transaction_id(transaction_id):
        logs = transaction_service.get_log_by_transaction_id(transaction_id)
        if logs:
            return jsonify(logs), 200
        return jsonify({"error": "Logs not found"}), 404

    @app.route("/insert", methods=["POST"])
    def insert_into_table_real():
        data = request.get_json()
        transaction_service.insert_into_table(data['table_name'], data['column_list'], data['value_list'])
        return jsonify({"Success": True}), 201

    @app.route("/transactions/count", methods=["POST"])
    def count_transaction():
        data = request.get_json()
        counted = transaction_service.count_transaction(data['column_name'], data['operation'])
        return jsonify(counted), 201

    @app.route("/create/tables", methods=["POST"])
    def create_tables():
        transaction_service.create_tables()
        return jsonify({'Success': True}), 201