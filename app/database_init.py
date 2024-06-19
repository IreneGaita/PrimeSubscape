import csv
import os
import random
import pandas as pd
from flask import current_app
from pymongo import MongoClient
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni l'URI di MongoDB dal file .env
MONGO_URI = os.getenv("MONGO_URI")

# Connetti a MongoDB
client = MongoClient(MONGO_URI)

def load_csv_to_mongo(csv_file_path):
    db = current_app.config["DB"]

    # Nome della collezione dove caricare i dati
    collection_name = 'amazon_prime_users'
    collection = db[collection_name]

    # Caricamento del file CSV
    data = pd.read_csv(csv_file_path)

    # Conversione delle date
    data['Date of Birth'] = pd.to_datetime(data['Date of Birth'], errors='coerce')
    data['Membership Start Date'] = pd.to_datetime(data['Membership Start Date'], errors='coerce')
    data['Membership End Date'] = pd.to_datetime(data['Membership End Date'], errors='coerce')

    # Mappatura delle frequenze di utilizzo
    frequency_mapping = {
        'Rarely': 1,
        'Occasional': 2,
        'Regular': 3,
        'Frequent': 4,
        'Very Frequent': 5
    }
    
    data['Usage Frequency'] = data['Usage Frequency'].map(frequency_mapping)

    # Creazione dei documenti embedded
    embedded_documents = data.apply(create_embedded_document, axis=1).tolist()

    if embedded_documents:
        # Se ci sono già dati nella collection, non inserirli
        if collection.count_documents({}) > 0:
            print(f"Data already exists in the '{collection_name}' collection.")
            return f"Data already exists in the '{collection_name}' collection."

        collection.insert_many(embedded_documents)
        print(f"Inserted {len(embedded_documents)} records into the '{collection_name}' collection.")
        return f"Inserted {len(embedded_documents)} records into the '{collection_name}' collection."
    else:
        print("No data found in the CSV file.")
        return "No data found in the CSV file."


# Funzione per creare il documento embedded
def create_embedded_document(row):
    #for all the rows , in device used column, add some random devices
    devices = ['Smart TV', 'Laptop', 'Tablet', 'Smartphone']
    #pick a random number of devices
    num_devices = random.randint(1, len(devices))
    #pick random devices
    row['Devices Used'] = random.sample(devices, num_devices)
    
    #for all the rows , in favorite genres column, add some random genres
    genres = ['Documentary', 'Horror', 'Comedy', 'Drama', 'Action', 'Sci-Fi','Romance']
    #pick a random number of genres
    num_genres = random.randint(1, len(genres))
    #pick random genres
    row['Favorite Genres'] = random.sample(genres, num_genres)
    
    purchase_history = ['Electronics', 'Books', 'Clothing']
    #pick a random number of genres
    num_purchase = random.randint(1, len(purchase_history))
    #pick random genres
    row['Purchase History'] = random.sample(purchase_history, num_purchase)
    
    return {
        "User ID": row['User ID'],
        "Name": row['Name'],
        "Email Address": row['Email Address'],
        "Username": row['Username'],
        "Date of Birth": row['Date of Birth'],
        "Gender": row['Gender'],
        "Location": row['Location'],
        "Subscription": {
            "Start Date": row['Membership Start Date'],
            "End Date": row['Membership End Date'],
            "Plan": row['Subscription Plan'],
            "Payment Information": row['Payment Information'],
            "Renewal Status": row['Renewal Status']
        },
        "Usage": {
            "Frequency": row['Usage Frequency'],
            "Purchase History": row['Purchase History'],
            "Favorite Genres": row['Favorite Genres'],
            "Devices Used": row['Devices Used'],
            "Engagement Metrics": row['Engagement Metrics']
        },
        "Feedback": {
            "Ratings": row['Feedback/Ratings'],
            "Customer Support Interactions": row['Customer Support Interactions']
        }
    }