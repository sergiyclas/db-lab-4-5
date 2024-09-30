# from flask import Blueprint, jsonify, request
# from my_project.auth.service.user_service import UserService
#
# user_blueprint = Blueprint('user', __name__)
#
# @user_blueprint.route('/users', methods=['GET'])
# def get_users():
#     users = get_all_users()
#     return jsonify(users)
#
# @user_blueprint.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     add_user(data)
#     return jsonify({"message": "User added successfully"})
