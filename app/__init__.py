from flask import Flask
from pymongo.mongo_client import MongoClient
import logging
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.init_app(app)  # Initialize logging

    # Initialize MongoDB connection
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.PrimeSubscape  # or client['your_database_name']
        app.logger.info("Connected to MongoDB successfully.")
    except Exception as e:
        app.logger.error("Failed to connect to MongoDB.")
        app.logger.error(e)
        db = None

    # Attach the db object to app so it can be accessed later
    app.config['DB'] = db

    with app.app_context():
        from . import routes  # Import routes

    return app
