class User:
    def __init__(self, id, username, email, password, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }
