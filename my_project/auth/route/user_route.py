from flask import request, jsonify
from my_project.auth.service.user_service import CustomerService, AccountService, TransactionService

# Ініціалізація сервісів
customer_service = CustomerService()
account_service = AccountService()
transaction_service = TransactionService()

def init_routes(app):
    # Маршрути для клієнтів
    @app.route("/customers", methods=["GET"])
    def get_customers():
        customers = customer_service.get_all_customers()
        return jsonify([customer.to_dict() for customer in customers])

    @app.route("/customers/<int:customer_id>", methods=["GET"])
    def get_customer(customer_id):
        customer = customer_service.get_customer_by_id(customer_id)
        if customer:
            return jsonify(customer.to_dict())
        return jsonify({"error": "Customer not found"}), 404

    @app.route("/customers", methods=["POST"])
    def create_customer():
        data = request.get_json()
        customer_id = customer_service.create_customer(data['customer_name'], data['email'], data['phone'])
        return jsonify({"id": customer_id}), 201

    @app.route("/customers/<int:customer_id>", methods=["PUT"])
    def update_customer(customer_id):
        data = request.get_json()
        customer_service.update_customer(customer_id, data['customer_name'], data['email'], data['phone'])
        return jsonify({"message": "Customer updated successfully"})

    @app.route("/customers/<int:customer_id>", methods=["DELETE"])
    def delete_customer(customer_id):
        customer_service.delete_customer(customer_id)
        return jsonify({"message": "Customer deleted successfully"})

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
        account_id = account_service.create_account(data['customer_id'], data['account_number'], data['balance'])
        return jsonify({"id": account_id}), 201

    @app.route("/accounts/<int:account_id>", methods=["PUT"])
    def update_account(account_id):
        data = request.get_json()
        account_service.update_account(account_id, data['account_number'], data['balance'])
        return jsonify({"message": "Account updated successfully"})

    @app.route("/accounts/<int:account_id>", methods=["DELETE"])
    def delete_account(account_id):
        account_service.delete_account(account_id)
        return jsonify({"message": "Account deleted successfully"})

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




# from flask import request, jsonify
# from my_project.auth.service.user_service import UserService
#
# user_service = UserService()

# def init_routes(app):
#     @app.route("/users", methods=["GET"])
#     def get_users():
#         users = user_service.get_all_users()
#         return jsonify([user.to_dict() for user in users])
#
#     @app.route("/users/<int:user_id>", methods=["GET"])
#     def get_user(user_id):
#         user = user_service.get_user_by_id(user_id)
#         if user:
#             return jsonify(user.to_dict())
#         return jsonify({"error": "User not found"}), 404
#
#     @app.route("/users", methods=["POST"])
#     def create_user():
#         data = request.get_json()
#         user_id = user_service.create_user(data['username'], data['email'], data['password'])
#         return jsonify({"id": user_id}), 201
#
#     @app.route("/users/<int:user_id>", methods=["PUT"])
#     def update_user(user_id):
#         data = request.get_json()
#         user_service.update_user(user_id, data['username'], data['email'], data['password'])
#         return jsonify({"message": "User updated successfully"})
#
#     @app.route("/users/<int:user_id>", methods=["DELETE"])
#     def delete_user(user_id):
#         user_service.delete_user(user_id)
#         return jsonify({"message": "User deleted successfully"})