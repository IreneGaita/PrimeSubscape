import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('MONGO_URI')
    DEBUG = True

    # Configurazione del logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @classmethod
    def init_app(cls, app):
        import logging
        from logging import StreamHandler

        handler = StreamHandler()
        handler.setLevel(cls.LOG_LEVEL)
        handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))

        app.logger.addHandler(handler)
        app.logger.setLevel(cls.LOG_LEVEL)
