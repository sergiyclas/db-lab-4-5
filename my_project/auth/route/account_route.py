from flask import request, jsonify
from my_project.auth.service.user_service import AccountService
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

account_service = AccountService()

def init_account_routes(app):
    @app.route("/login", methods=["POST"])
    def login():
        """
        Login to get JWT token
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [username, password]
              properties:
                username: {type: string, example: "admin"}
                password: {type: string, example: "123456"}
        responses:
          200:
            description: Token successfully created
            schema:
              type: object
              properties:
                access_token: {type: string}
          401:
            description: Invalid credentials
        """
        username = request.json.get("username")
        password = request.json.get("password")

        if username == "admin" and password == "123456":
            token = create_access_token(identity=username)
            return jsonify(access_token=token)
        return jsonify({"msg": "Bad credentials"}), 401

    @app.route("/accounts", methods=["GET"])
    @jwt_required()
    def get_accounts():
        """
        Get all accounts
        ---
        tags:
          - Accounts
        security:
          - BearerAuth: []
        responses:
          200:
            description: A list of accounts
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  customer_id:
                    type: integer
                    example: 1
                  account_number:
                    type: string
                    example: "ACC10001"
                  balance:
                    type: number
                    format: float
                    example: 5000.00
        """
        accounts = account_service.get_all_accounts()
        return jsonify([account.to_dict() for account in accounts])

    @app.route("/accounts/<int:account_id>", methods=["GET"])
    @jwt_required()
    def get_account(account_id):
        """
        Get account by ID
        ---
        tags:
          - Accounts
        security:
          - BearerAuth: []
        parameters:
          - name: account_id
            in: path
            type: integer
            required: true
            description: ID of the account
        responses:
          200:
            description: Account details
            schema:
              type: object
              properties:
                id: {type: integer, example: 1}
                customer_id: {type: integer, example: 1}
                account_number: {type: string, example: "ACC10001"}
                balance: {type: number, example: 5000.00}
          404:
            description: Account not found
        """
        account = account_service.get_account_by_id(account_id)
        if account:
            return jsonify(account.to_dict())
        return jsonify({"error": "Account not found"}), 404

    @app.route("/accounts", methods=["POST"])
    @jwt_required()
    def create_account():
        """
        Create a new account
        ---
        tags:
          - Accounts
        security:
          - BearerAuth: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [customer_id, account_number, balance]
              properties:
                customer_id: {type: integer, example: 1}
                account_number: {type: string, example: "ACC20001"}
                balance: {type: number, example: 10000.00}
        responses:
          201:
            description: Account created successfully
            schema:
              type: object
              properties:
                id: {type: integer, example: 13}
        """
        data = request.get_json()
        account_id = account_service.create_account(
            data['customer_id'], data['account_number'], data['balance']
        )
        return jsonify({"id": account_id}), 201

    @app.route("/accounts/<int:account_id>", methods=["PUT"])
    def update_account(account_id):
        """
        Update account details
        ---
        tags:
          - Accounts
        parameters:
          - name: account_id
            in: path
            type: integer
            required: true
            description: ID of the account
          - in: body
            name: body
            required: true
            schema:
              type: object
              required: [customer_id, account_number, balance]
              properties:
                customer_id: {type: integer, example: 2}
                account_number: {type: string, example: "ACC50001"}
                balance: {type: number, example: 7500.75}
        responses:
          200:
            description: Account updated successfully
            schema:
              type: object
              properties:
                message: {type: string, example: "Account updated successfully"}
        """
        data = request.get_json()
        account_service.update_account(account_id, data['customer_id'], data['account_number'], data['balance'])
        return jsonify({"message": "Account updated successfully"})

    @app.route("/accounts/<int:account_id>", methods=["DELETE"])
    def delete_account(account_id):
        """
        Delete account
        ---
        tags:
          - Accounts
        parameters:
          - name: account_id
            in: path
            type: integer
            required: true
            description: ID of the account
        responses:
          200:
            description: Account deleted successfully
            schema:
              type: object
              properties:
                message: {type: string, example: "Account deleted successfully"}
        """
        account_service.delete_account(account_id)
        return jsonify({"message": "Account deleted successfully"})

    @app.route("/customers/<int:customer_id>/accounts", methods=["GET"])
    def get_accounts_for_customer(customer_id):
        """
        Get accounts for a specific customer
        ---
        tags:
          - Accounts
        parameters:
          - name: customer_id
            in: path
            type: integer
            required: true
            description: ID of the customer
        responses:
          200:
            description: A list of accounts for the customer
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer, example: 1}
                  customer_id: {type: integer, example: 1}
                  account_number: {type: string, example: "ACC10001"}
                  balance: {type: number, example: 5000.00}
        """
        accounts = account_service.get_accounts_by_customer_id(customer_id)
        return jsonify(accounts)
