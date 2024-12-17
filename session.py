# session.py


class UserSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._instance.user_id = None
            cls._instance.username = None
            cls._instance.is_admin = False
        return cls._instance

    def set_user(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.is_admin = username == "admin"

    def clear_user(self):
        self.user_id = None
        self.username = None
        self.is_admin = False
