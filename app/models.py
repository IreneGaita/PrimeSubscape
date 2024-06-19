from flask import current_app

db = current_app.config['DB']["amazon_prime_users"]

def add_user(name, email, password):
    user = {
        'Name': name,
        'Email address': email,
        'password': password
    }
    db.insert_one(user)
    return 'User added successfully!'

def search_user(name):
    user={
        'Name' : name
    }
    find_user=db.find_one(user)

    return find_user 