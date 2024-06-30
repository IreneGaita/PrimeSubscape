from datetime import datetime, timedelta
import random
import re
from bson import ObjectId
from flask import current_app

db = current_app.config['DB']["amazon_prime_users"]

def find_user_by_id(user_id):
    user = {
        '_id': ObjectId(user_id)
    }
    return db.find_one(user)

def search_user(name):
    # Creazione del pattern regex per la ricerca
    regex_pattern = re.compile(name, re.IGNORECASE)  # Ignora maiuscole e minuscole

    # Crea il filtro di ricerca utilizzando $regex
    query = {
        'Name': {
            '$regex': regex_pattern
        }
    }
    
    return list(db.find(query))

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
    
    showexpired_users= list(db.find({'Subscription.End Date': {"$lte": datetime.now()}}))
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

def show_ratings_lower(rating,interactionsupp):
    query = {
        '$or': [
            { 'Feedback.Ratings': { '$lt': rating } },
            { 'Feedback.Customer Support Interactions': { '$gt': interactionsupp } }
        ]
    }
    print(query)
    rating_user=list(db.find(query))
    print(rating_user)
    return rating_user

def count_plans():
    pipeline = [
        {
            '$group': {
                '_id': "$Subscription.Plan",
                'count': { '$sum': 1 }
            }
        }
    ]
    print(pipeline)
    count_p=list(db.aggregate(pipeline))
    print(count_p)
    return count_p


def rating_by_location():
    pipeline = [
        {
            '$group': {
                '_id': "$Location",
                'avgRating': { '$avg': "$Feedback.Ratings" }
            }
        },
        {
            '$sort': { 'avgRating': 1 }  # Ordina in ordine crescente
        }
    ]
    avg_ratings = list(db.aggregate(pipeline))  
    return avg_ratings


def find_users_with_one_device():
    query = {
        "Usage.Devices Used": { '$size': 1 }
    }
    result = list(db.find(query))  
    return result


def user_monthly_plan_frequency():
    query = {
        '$and': [
            { "Subscription.Plan": "Monthly" },
            { "Usage.Frequency": { '$gt': 2 } }
        ]
        
    }
    sort= [("Usage.Frequency", -1)]
    result = list(db.find(query).sort(sort)) 
    return result


def count_renewal_status():
    pipeline = [
        {
            '$group': {
                '_id': "$Subscription.Renewal Status",
                'count': { '$sum': 1 }
            }
        }
    ]
    result = list(db.aggregate(pipeline)) 
    return result

def get_unique_genres():
    return db.distinct("Usage.Favorite Genres")  
def find_users_with_favorite_genres(genres):

    query = { "Usage.Favorite Genres": { '$in': genres } }
    return list(db.find(query))  



def count_devices_used():
    pipeline = [
        {
            '$group': {
                '_id': { '$size': "$Usage.Devices Used" },
                'count': { '$sum': 1 }
            }
        }
    ]
    return list(db.aggregate(pipeline)) 


def aggregate_subscription_years():

    # Definisci la pipeline di aggregazione
    # Definisci la pipeline di aggregazione
    pipeline = [
        {
            "$addFields": {
                "Subscription.Years": {
                    "$divide": [
                        {"$subtract": ["$Subscription.End Date", "$Subscription.Start Date"]},
                        1000 * 60 * 60 * 24 * 365  # Convertire millisecondi in anni
                    ]
                }
            }
        },
        {
            "$project": {
                "User ID": 1,
                "Subscription.Years": 1,
                "Name": 1,
            }
        }
    ]


    # Esegui l'aggregazione
    result = db.aggregate(pipeline)
    # Ritorna i risultati come lista
    return list(result)


def find_every_user_less_greater_equal_subscription_years(operator, years):
    # Definisci la pipeline di aggregazione
    pipeline = [
        {
            "$addFields": {
                "Subscription.Years": {
                    "$divide": [
                        {"$subtract": ["$Subscription.End Date", "$Subscription.Start Date"]},
                        1000 * 60 * 60 * 24 * 365  # Convertire millisecondi in anni
                    ]
                }
            }
        },
        {
            "$match": {
                "Subscription.Years": { f"${operator}": years }
            }
        }
    ]
    
    # Aggiungi una condizione personalizzata per l'operatore "eq"
    if operator == "eq":
        pipeline[1]["$match"]["Subscription.Years"] = {
            "$gte": years - 1/12,
            "$lte": years + 1/12
        }
    
    # Esegui l'aggregazione
    result = db.aggregate(pipeline)
    # Ritorna i risultati come lista
    return list(result)

    