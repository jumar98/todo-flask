from flask_login import UserMixin
from app.firestore_service import get_user


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserModel(UserMixin):

    def __init__(self, user):
        self.id = user.username
        self.password = user.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user = User(user_doc.id, user_doc.to_dict()['password'])
        return UserModel(user)
