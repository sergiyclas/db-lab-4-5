from flask import Flask
from my_project.auth.route.user_route import init_routes
from config import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ініціалізація конфігурації
# app.config.from_pyfile('config/app.yml')
db_config = config.load_db_config()

# Ініціалізація маршрутів
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
