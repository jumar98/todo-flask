import firebase_admin
from firebase_admin import credentials, firestore

credentials = credentials.ApplicationDefault()
firebase_admin.initialize_app(credentials)

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user(user_id):
    return db.collection('users').document(user_id).get()


def get_tasks(user_id):
    return db.collection('users')\
           .document(user_id).collection('tasks').get()