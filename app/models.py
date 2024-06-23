import random
from bson import ObjectId
from flask import current_app

db = current_app.config['DB']["amazon_prime_users"]

def find_user_by_id(user_id):
    user = {
        '_id': ObjectId(user_id)
    }
    return db.find_one(user)

def search_user(name):
    user = {
        'Name': name
    }
    #print all user object id
    for user in db.find(user):
        print(user['_id'])
    return list(db.find(user))

def edit_user(user_data, user_id):
    db.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
    return "User updated successfully!"

def delete_user(user_id):
    user = {
        '_id': ObjectId(user_id)
    }
    db.delete_one(user)
    return 'User deleted successfully!'

def search_all_user():
    return list(db.find({}))

def add_user(user_data):
    #create random id for the user which is unique
    user_data['_id'] = ObjectId()
    
    #check if the random id is unique
    while db.find_one({'_id': user_data['_id']}):
        user_data['_id'] = ObjectId()
    

    user_data['User ID'] = random.randint(1000, 9999)

    #check if the user id is unique
    while db.find_one({'User ID': user_data['User ID']}):
        user_data['User ID'] = random.randint(1000, 9999)

    result = db.insert_one(user_data)
    return result