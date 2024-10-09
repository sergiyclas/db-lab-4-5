from flask import request, jsonify
from my_project.auth.service.user_service import AccountService

account_service = AccountService()

def init_account_routes(app):
    # Маршрути для рахунків
    @app.route("/accounts", methods=["GET"])
    def get_accounts():
        accounts = account_service.get_all_accounts()
        return jsonify([account.to_dict() for account in accounts])

    @app.route("/accounts/<int:account_id>", methods=["GET"])
    def get_account(account_id):
        account = account_service.get_account_by_id(account_id)
        if account:
            return jsonify(account.to_dict())
        return jsonify({"error": "Account not found"}), 404

    @app.route("/accounts", methods=["POST"])
    def create_account():
        data = request.get_json()
        print(data)
        account_id = account_service.create_account(data['customer_id'], data['account_number'], data['balance'])
        return jsonify({"id": account_id}), 201

    @app.route("/accounts/<int:account_id>", methods=["PUT"])
    def update_account(account_id):
        data = request.get_json()
        account_service.update_account(account_id, data['customer_id'], data['account_number'], data['balance'])
        return jsonify({"message": "Account updated successfully"})

    @app.route("/accounts/<int:account_id>", methods=["DELETE"])
    def delete_account(account_id):
        account_service.delete_account(account_id)
        return jsonify({"message": "Account deleted successfully"})

    @app.route("/customers/<int:customer_id>/accounts", methods=["GET"])
    def get_accounts_for_customer(customer_id):
        accounts = account_service.get_accounts_by_customer_id(customer_id)
        if not isinstance(accounts, list):
            accounts = [accounts]
        return jsonify([account.to_dict() for account in accounts])
