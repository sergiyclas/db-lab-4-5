from my_project.auth.domain.domains import (
    PaymentTemplate,
)
from my_project.auth.dao.Base_dao import BaseDAO

class PaymentTemplateDAO(BaseDAO):
    def get_all_payment_templates(self):
        self.cursor.execute("SELECT * FROM payment_templates")
        result = self.cursor.fetchall()
        return [PaymentTemplate(**row) for row in result]

    def get_payment_template_by_id(self, template_id):
        self.cursor.execute("SELECT * FROM payment_templates WHERE template_id = %s", (template_id,))
        row = self.cursor.fetchone()
        if row:
            return PaymentTemplate(**row)
        return None

    def create_payment_template(self, account_id, template_name, template_details):
        self.cursor.execute(
            "INSERT INTO payment_templates (account_id, template_name, template_details) VALUES (%s, %s, %s)",
            (account_id, template_name, template_details)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def delete_payment_template(self, template_id):
        self.cursor.execute("DELETE FROM payment_templates WHERE template_id = %s", (template_id,))
        self.connection.commit()