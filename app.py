from flask import Flask

from my_project.database.tables import setup_tables
from my_project.database.triggers import setup_triggers, drop_triggers
from my_project.database.procedures import setup_procedures
from my_project.database.functions import setup_functions
from config import config
from flask_cors import CORS
import mysql.connector
from flasgger import Swagger
from db import main

app = Flask(__name__)
main()

Swagger(app)
CORS(app)

# Завантаження конфігурації бази даних
db_config = config.load_db_config()
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

drop_triggers(cursor)
# # Налаштування бази даних
# setup_tables(cursor)
# setup_triggers(cursor)
# setup_procedures(cursor)
# setup_functions(cursor)
db_connection.commit()

from my_project.auth.route.customer_route import init_customer_routes
from my_project.auth.route.account_route import init_account_routes
from my_project.auth.route.transaction_route import init_transaction_routes
from my_project.auth.route.transactionAccount_route import init_transaction_account_routes

# Ініціалізація маршрутів
init_customer_routes(app)
init_account_routes(app)
init_transaction_routes(app)
init_transaction_account_routes(app)

# Закриття з’єднання після ініціалізації
cursor.close()
db_connection.close()

if __name__ == "__main__":
    app.run(debug=True)
