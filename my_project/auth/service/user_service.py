from my_project.auth.dao.user_dao import UserDAO

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def get_all_users(self):
        return self.user_dao.get_all_users()

    def get_user_by_id(self, user_id):
        return self.user_dao.get_user_by_id(user_id)

    def create_user(self, username, email, password):
        return self.user_dao.create_user(username, email, password)

    def update_user(self, user_id, username, email, password):
        self.user_dao.update_user(user_id, username, email, password)

    def delete_user(self, user_id):
        self.user_dao.delete_user(user_id)
