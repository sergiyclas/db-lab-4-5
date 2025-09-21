from flask import request, jsonify
from my_project.auth.service.user_service import CustomerService
from flasgger import swag_from

customer_service = CustomerService()

def init_customer_routes(app):
    # Routes for Customers
    @app.route("/customers", methods=["GET"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Get all customers',
        'description': 'Retrieve the list of all customers from the system.',
        'responses': {
            200: {
                'description': 'A list of customers',
                'content': {
                    'application/json': {
                        'example': [
                            {"id": 1, "customer_name": "John Doe", "email": "john@example.com", "phone": "1234567890"}
                        ]
                    }
                }
            }
        }
    })
    def get_customers():
        customers = customer_service.get_all_customers()
        return jsonify(customers)

    @app.route("/customers/<int:customer_id>", methods=["GET"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Get customer by ID',
        'description': 'Retrieve details of a specific customer using their ID.',
        'parameters': [
            {
                'name': 'customer_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the customer',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Customer details',
                'content': {
                    'application/json': {
                        'example': {"id": 1, "customer_name": "John Doe", "email": "john@example.com", "phone": "1234567890"}
                    }
                }
            },
            404: {'description': 'Customer not found'}
        }
    })
    def get_customer(customer_id):
        customer = customer_service.get_customer_by_id(customer_id)
        if customer:
            return jsonify(customer.to_dict())
        return jsonify({"error": "Customer not found"}), 404

    @app.route("/customers", methods=["POST"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Create a new customer',
        'description': 'Create a new customer by providing their name, email, and phone number.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {
                        "customer_name": "Jane Smith",
                        "email": "jane@example.com",
                        "phone": "9876543210"
                    }
                }
            }
        },
        'responses': {
            201: {
                'description': 'Customer successfully created',
                'content': {
                    'application/json': {
                        'example': {"id": 2}
                    }
                }
            }
        }
    })
    def create_customer():
        data = request.get_json()
        customer_id = customer_service.create_customer(data['customer_name'], data['email'], data['phone'])
        return jsonify({"id": customer_id}), 201

    @app.route("/customers/<int:customer_id>", methods=["PUT"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Update an existing customer',
        'description': 'Update the details of an existing customer using their ID.',
        'parameters': [
            {
                'name': 'customer_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the customer to update',
                'schema': {'type': 'integer'}
            }
        ],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {
                        "customer_name": "Jane Smith",
                        "email": "jane_new@example.com",
                        "phone": "1112223333"
                    }
                }
            }
        },
        'responses': {
            200: {
                'description': 'Customer successfully updated',
                'content': {
                    'application/json': {
                        'example': {"message": "Customer updated successfully"}
                    }
                }
            },
            404: {'description': 'Customer not found'}
        }
    })
    def update_customer(customer_id):
        data = request.get_json()
        customer_service.update_customer(customer_id, data['customer_name'], data['email'], data['phone'])
        return jsonify({"message": "Customer updated successfully"}), 200

    @app.route("/customers/<int:customer_id>", methods=["DELETE"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Delete a customer',
        'description': 'Delete an existing customer from the system using their ID.',
        'parameters': [
            {
                'name': 'customer_id',
                'in': 'path',
                'required': True,
                'description': 'The ID of the customer to delete',
                'schema': {'type': 'integer'}
            }
        ],
        'responses': {
            200: {
                'description': 'Customer successfully deleted',
                'content': {
                    'application/json': {
                        'example': {"message": "Customer deleted successfully"}
                    }
                }
            },
            404: {'description': 'Customer not found'}
        }
    })
    def delete_customer(customer_id):
        customer_service.delete_customer(customer_id)
        return jsonify({"message": "Customer deleted successfully"})

    @app.route("/customers/noname", methods=["POST"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Create customer without a name',
        'description': 'Create a customer without providing a name, using only a start and end date.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"start": "2024-01-01", "end": "2024-12-31"}
                }
            }
        },
        'responses': {
            201: {
                'description': 'Customer created without name',
                'content': {
                    'application/json': {
                        'example': {"Success": True}
                    }
                }
            }
        }
    })
    def create_customer_noname():
        data = request.get_json()
        customer_service.create_customer_noname(data['start'], data['end'])
        return jsonify({"Success": True}), 201

    @app.route("/allowed_names", methods=["POST"])
    @swag_from({
        'tags': ['Customers'],
        'summary': 'Insert a name into allowed names',
        'description': 'Add a new allowed name to the system.',
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {"name": "Alice"}
                }
            }
        },
        'responses': {
            201: {
                'description': 'Name successfully added to allowed names',
                'content': {
                    'application/json': {
                        'example': {"id": 10}
                    }
                }
            }
        }
    })
    def insert_in_allowed_names():
        data = request.get_json()
        customer_id = customer_service.insert_in_allowed_names(data['name'])
        return jsonify({"id": customer_id}), 201
