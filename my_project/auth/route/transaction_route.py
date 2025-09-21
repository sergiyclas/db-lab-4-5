from flask import request, jsonify
from my_project.auth.service.user_service import TransactionService
from flasgger import swag_from

transaction_service = TransactionService()

def init_transaction_routes(app):
    # Routes for Transactions
    @app.route("/transactions", methods=["GET"])
    @swag_from({
        'tags': ['Transactions'],
        'summary': 'Get all transactions',
        'description': 'Retrieve the list of all transactions from the system.',
        'responses': {
            200: {
                'description': 'A list of transactions',
                'content': {
                    'application/json': {
                        'example': [
                            {"id": 1, "amount": 100.50, "transaction_date": "2024-01-01"}
                        ]
                    }
                }
            }
        }
    })
    def get_transactions():
        transactions = transaction_service.get_all_transactions()
        return jsonify([transaction.to_dict() for transaction in transactions])

    @app.route("/transactions/<int:transaction_id>", methods=["GET"])
    @swag_from({
        'tags': ['Transactions'],
        'summary': 'Get transaction by ID',
        'description': 'Retrieve details of a specific transaction using its ID.',
        'parameters': [
            {
                'name': 'transaction_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the transaction',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Transaction details',
                'content': {
                    'application/json': {
                        'example': {"id": 1, "amount": 100.50, "transaction_date": "2024-01-01"}
                    }
                }
            },
            404: {'description': 'Transaction not found'}
        }
    })
    def get_transaction(transaction_id):
        transaction = transaction_service.get_transaction_by_id(transaction_id)
        if transaction:
            return jsonify(transaction.to_dict())
        return jsonify({"error": "Transaction not found"}), 404

    @app.route("/transactions", methods=["POST"])
    @swag_from({
        'tags': ['Transactions'],
        'summary': 'Create a new transaction',
        'description': 'Create a new transaction by providing the amount and transaction date.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"amount": 200.75, "transaction_date": "2024-05-15"}
                }
            }
        },
        'responses': {
            201: {
                'description': 'Transaction successfully created',
                'content': {
                    'application/json': {
                        'example': {"id": 2}
                    }
                }
            }
        }
    })
    def create_transaction():
        data = request.get_json()
        transaction_id = transaction_service.create_transaction(data['amount'], data['transaction_date'])
        return jsonify({"id": transaction_id}), 201

    @app.route("/transactions/<int:transaction_id>", methods=["PUT"])
    @swag_from({
        'tags': ['Transactions'],
        'summary': 'Update an existing transaction',
        'description': 'Update the details of an existing transaction using its ID.',
        'parameters': [
            {
                'name': 'transaction_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the transaction to update',
                'schema': {'type': 'integer'}
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"amount": 300.10, "transaction_date": "2024-06-01"}
                }
            }
        },
        'responses': {
            200: {
                'description': 'Transaction successfully updated',
                'content': {
                    'application/json': {
                        'example': {"message": "Transaction updated successfully"}
                    }
                }
            },
            404: {'description': 'Transaction not found'}
        }
    })
    def update_transaction(transaction_id):
        data = request.get_json()
        transaction_service.update_transaction(transaction_id, data['amount'], data['transaction_date'])
        return jsonify({"message": "Transaction updated successfully"})

    @app.route("/transactions/<int:transaction_id>", methods=["DELETE"])
    @swag_from({
        'tags': ['Transactions'],
        'summary': 'Delete a transaction',
        'description': 'Delete an existing transaction from the system using its ID.',
        'parameters': [
            {
                'name': 'transaction_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the transaction to delete',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Transaction successfully deleted',
                'content': {
                    'application/json': {
                        'example': {"message": "Transaction deleted successfully"}
                    }
                }
            },
            404: {'description': 'Transaction not found'}
        }
    })
    def delete_transaction(transaction_id):
        transaction_service.delete_transaction(transaction_id)
        return jsonify({"message": "Transaction deleted successfully"})

    @app.route("/logs", methods=["GET"])
    @swag_from({
        'tags': ['Logs'],
        'summary': 'Get all logs',
        'description': 'Retrieve the list of all logs from the system.',
        'responses': {
            200: {
                'description': 'A list of logs',
                'content': {
                    'application/json': {
                        'example': [
                            {"id": 1, "transaction_id": 1, "action": "CREATED", "timestamp": "2024-01-01T12:00:00"}
                        ]
                    }
                }
            }
        }
    })
    def get_logs():
        logs = transaction_service.get_all_logs()
        return jsonify([log.to_dict() for log in logs])

    @app.route("/logs/<int:transaction_id>/transactions", methods=["GET"])
    @swag_from({
        'tags': ['Logs'],
        'summary': 'Get logs by transaction ID',
        'description': 'Retrieve all logs related to a specific transaction.',
        'parameters': [
            {
                'name': 'transaction_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the transaction to fetch logs for',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Logs related to the transaction',
                'content': {
                    'application/json': {
                        'example': [
                            {"id": 1, "transaction_id": 1, "action": "UPDATED", "timestamp": "2024-01-02T14:30:00"}
                        ]
                    }
                }
            },
            404: {'description': 'Logs not found'}
        }
    })
    def get_logs_by_transaction_id(transaction_id):
        logs = transaction_service.get_log_by_transaction_id(transaction_id)
        if logs:
            return jsonify(logs), 200
        return jsonify({"error": "Logs not found"}), 404


    @app.route("/insert", methods=["POST"])
    @swag_from({
        'tags': ['Database'],
        'summary': 'Insert a new row into a specified table',
        'description': (
                "This endpoint allows inserting a new row into a database table by calling a stored procedure. "
                "The client must provide the table name, a list of columns, and a corresponding list of values. "
                "The backend calls a stored procedure `insert_into_table` with these parameters to perform the insertion. "
                "All operations are executed within the database, and no data validation is performed here, "
                "so ensure that the column names and values match the table schema."
        ),
        'parameters': [
            {
                'name': 'transaction_id',
                'in': 'path',
                'required': True,
                'description': 'ID of the transaction to retrieve',
                'schema': {'type': 'integer'}
            }
        ],

        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {
                        "table_name": "transactions",
                        "column_list": ["amount", "transaction_date"],
                        "value_list": [500.25, "2024-07-01"]
                    },
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'table_name': {'type': 'string',
                                           'description': 'The name of the table where data will be inserted'},
                            'column_list': {'type': 'array', 'items': {'type': 'string'},
                                            'description': 'List of column names for insertion'},
                            'value_list': {'type': 'array', 'items': {'type': 'string'},
                                           'description': 'List of values to insert corresponding to columns'}
                        },
                        'required': ['table_name', 'column_list', 'value_list']
                    }
                }
            }
        },
        'responses': {
            201: {
                'description': 'Data successfully inserted via stored procedure',
                'content': {
                    'application/json': {'example': {"Success": True}}
                }
            },
            400: {
                'description': 'Invalid input or mismatch between columns and values',
                'content': {
                    'application/json': {'example': {"error": "Invalid input"}}
                }
            },
            500: {
                'description': 'Server error during insertion',
                'content': {
                    'application/json': {'example': {"error": "Something went wrong"}}
                }
            }
        }
    })
    def insert_into_table_real():
        """
        Endpoint to insert a new row into a specified table using a stored procedure.
        """
        data = request.get_json()
        transaction_service.insert_into_table(data['table_name'], data['column_list'], data['value_list'])
        return jsonify({"Success": True}), 201


    @app.route("/transactions/count", methods=["POST"])
    @swag_from({
        'tags': ['Transactions'],
        'summary': 'Count transactions',
        'description': 'Count transactions based on a column and operation (e.g., SUM, AVG).',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"column_name": "amount", "operation": "SUM"}
                }
            }
        },
        'responses': {
            201: {
                'description': 'Result of the count operation',
                'content': {
                    'application/json': {
                        'example': {"SUM": 1200.50}
                    }
                }
            }
        }
    })
    def count_transaction():
        data = request.get_json()
        counted = transaction_service.count_transaction(data['column_name'], data['operation'])
        return jsonify(counted), 201

    @app.route("/create/tables", methods=["POST"])
    @swag_from({
        'tags': ['Database'],
        'summary': 'Create database tables',
        'description': 'Create all necessary database tables for the application.',
        'responses': {
            201: {
                'description': 'Tables successfully created',
                'content': {
                    'application/json': {
                        'example': {"Success": True}
                    }
                }
            }
        }
    })
    def create_tables():
        transaction_service.create_tables()
        return jsonify({'Success': True}), 201
