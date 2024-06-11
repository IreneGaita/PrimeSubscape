from flask import current_app

db = current_app.config['DB'].users

def get_users():
    db = current_app.config['DB']
    if db is not None:
        users = db.users.find()
        return list(users)
    else:
        return []

def add_user(username, email, password):
    db = current_app.config['DB']
    if db is not None:
        user = {
            'username': username,
            'email': email,
            'password': password
        }
        db.users.insert_one(user)
    else:
        raise Exception("Database connection is not available")
