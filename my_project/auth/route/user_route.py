from flask import request, jsonify
from my_project.auth.service.user_service import UserService

user_service = UserService()

def init_routes(app):
    @app.route("/users", methods=["GET"])
    def get_users():
        users = user_service.get_all_users()
        return jsonify([user.to_dict() for user in users])

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = user_service.get_user_by_id(user_id)
        if user:
            return jsonify(user.to_dict())
        return jsonify({"error": "User not found"}), 404

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json()
        user_id = user_service.create_user(data['username'], data['email'], data['password'])
        return jsonify({"id": user_id}), 201

    @app.route("/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        data = request.get_json()
        user_service.update_user(user_id, data['username'], data['email'], data['password'])
        return jsonify({"message": "User updated successfully"})

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user_service.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"})

    # @app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
    # def handle_user(user_id):
    #     if request.method == "GET":
    #         user = user_service.get_user_by_id(user_id)
    #         if user:
    #             return jsonify(user.to_dict())
    #         return jsonify({"error": "User not found"}), 404
    #
    #     if request.method == "PUT":
    #         data = request.get_json()
    #         user_service.update_user(user_id, data['username'], data['email'], data['password'])
    #         return jsonify({"message": "User updated successfully"})
    #
    #     if request.method == "DELETE":
    #         user_service.delete_user(user_id)
    #         return jsonify({"message": "User deleted successfully"})