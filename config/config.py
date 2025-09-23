import yaml
import mysql.connector

def load_db_config():
    with open('config/app.yml', 'r') as file:
        config = yaml.safe_load(file)
        return config['database']

def connect_to_db():
    db_config = load_db_config()
    connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['db'],
        port=db_config['port']
    )
    return connection
