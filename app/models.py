from datetime import datetime
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


def show_end_date():
    current_date = datetime.now()
    current_date = current_date.strftime("%Y-%m-%d")
    showexpired_users= list(db.find({'Subscription.End Date': {"$lte": current_date}}))
    print(showexpired_users)
    return showexpired_users


def intervall_date(startDate, endDate):
    user= {
        'Subscription.Start Date': startDate,
        'Subscription.End Date': endDate
    }
    
    query= {"$and":[
        {'Subscription.Start Date': {"$gte": startDate}},{'Subscription.End Date': {"$lte": endDate}}
        ]}
    intervall_user=list(db.find(query
    ))
    print(query)
    print(startDate,endDate)
    print(intervall_user)
    return intervall_user

def show_gender(gender):
    query= {
        'Gender': gender
    }
    gender_user = list(db.find(query))
    return gender_user


def show_location(location):
    query= {
        'Location': { '$regex': f'^{location}', '$options': 'i'  }  
    }
   
    location_user = list(db.find(query))
    return location_user
