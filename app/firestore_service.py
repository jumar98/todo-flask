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


def create_user(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})


def create_task(user_id, description, done=False):
    task_collection_ref = db.collection('users').document(user_id).\
                          collection('tasks')
    task_collection_ref.add({'description': description, 'done': done})


def delete_task(user_id, task_id):
    task_ref = _get_task_ref(user_id, task_id)
    task_ref.delete()


def update_task(user_id, task_id, done):
    task_ref = _get_task_ref(user_id, task_id)
    task_ref.update({'done': not done})


def _get_task_ref(user_id, task_id):
    return db.document(f'users/{user_id}/tasks/{task_id}')
