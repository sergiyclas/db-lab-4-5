from flask import Blueprint
from my_project.auth.route.user_route import init_routes

auth_bp = Blueprint('auth', __name__)

init_routes(auth_bp)
