from flask import Flask
# from my_project.auth.route.user_route import init_routes
from my_project.auth.route.customer_route import init_customer_routes
from my_project.auth.route.account_route import init_account_routes
from my_project.auth.route.transaction_route import init_transaction_routes
from my_project.auth.route.transactionAccount_route import init_transaction_account_routes

from config import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# app.config.from_pyfile('config/app.yml')
db_config = config.load_db_config()

init_customer_routes(app)
init_account_routes(app)
init_transaction_routes(app)
init_transaction_account_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
