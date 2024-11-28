from my_project.auth.domain.domains import (
    Customer
)
from my_project.auth.dao.Base_dao import BaseDAO


class CustomerDAO(BaseDAO):
    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM customers")
        result = self.cursor.fetchall()
        return [Customer(**row) for row in result]

    def get_customer_by_id(self, customer_id):
        self.cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        row = self.cursor.fetchone()
        if row:
            return Customer(**row)
        return None

    def create_customer(self, customer_name, email, phone):
        self.cursor.execute(
            "INSERT INTO customers (customer_name, email, phone) VALUES (%s, %s, %s)",
            (customer_name, email, phone)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_in_allowed_names(self, name):
        self.cursor.execute(
            "INSERT INTO allowed_names (name) VALUES (%s);",
            (name,)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def create_customer_noname(self, start, end):
        self.cursor.execute(
            "CALL insert_multiple_rows_customers(%s, %s)",
            (start, end)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def update_customer(self, customer_id, customer_name, email, phone):
        query = "UPDATE customers SET customer_name = %s, email = %s, phone = %s WHERE customer_id = %s"
        self.cursor.execute(query, (customer_name, email, phone, customer_id))
        self.connection.commit()
        return self.cursor.lastrowid

    def delete_customer(self, customer_id):
        self.cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        self.connection.commit()
        return self.cursor.lastrowid