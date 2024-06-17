import csv
import os
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

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
        if data:
            #se ci sono già dati nella collection, non inserirli
            if collection.count_documents({}) > 0:
                print(f"Data already exists in the '{collection_name}' collection.")
                return f"Data already exists in the '{collection_name}' collection."
            
            collection.insert_many(data)
            print(f"Inserted {len(data)} records into the '{collection_name}' collection.")
        else:
            print("No data found in the CSV file.")
            return "No data found in the CSV file."
    
    return "Data loaded successfully."
