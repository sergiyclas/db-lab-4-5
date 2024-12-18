from flask import request, jsonify
from my_project.auth.service.user_service import CustomerService

customer_service = CustomerService()

def init_customer_routes(app):
    # Маршрути для клієнтів
    @app.route("/customers", methods=["GET"])
    def get_customers():
        customers = customer_service.get_all_customers()
        return jsonify(customers)

    @app.route("/customers/<int:customer_id>", methods=["GET"])
    def get_customer(customer_id):
        customer = customer_service.get_customer_by_id(customer_id)
        if customer:
            return jsonify(customer.to_dict())
        return jsonify({"error": "Customer not found"}), 404

    @app.route("/customers", methods=["POST"])
    def create_customer():
        data = request.get_json()
        customer_id = customer_service.create_customer(data['customer_name'], data['email'], data['phone'])
        return jsonify({"id": customer_id}), 201

    @app.route("/customers/<int:customer_id>", methods=["PUT"])
    def update_customer(customer_id):
        data = request.get_json()
        customer_service.update_customer(customer_id, data['customer_name'], data['email'], data['phone'])
        return jsonify({"message": "Customer updated successfully"}), 200

    @app.route("/customers/<int:customer_id>", methods=["DELETE"])
    def delete_customer(customer_id):
        customer_service.delete_customer(customer_id)
        return jsonify({"message": "Customer deleted successfully"})

    @app.route("/customers/noname", methods=["POST"])
    def create_customer_noname():
        data = request.get_json()
        customer_service.create_customer_noname(data['start'], data['end'])
        return jsonify({"Success": True}), 201

    @app.route("/allowed_names", methods=["POST"])
    def insert_in_allowed_names():
        data = request.get_json()
        customer_id = customer_service.insert_in_allowed_names(data['name'])
        return jsonify({"id": customer_id}), 201