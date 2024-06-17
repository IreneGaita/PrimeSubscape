from flask import render_template
from flask import current_app as app
from app.models import add_user, get_users
from app.database_init import load_csv_to_mongo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prova')
def prova_db():
    # crea una nuova collection
    add_user('mario', 'mario@gmail.com', '1234')
    
    # stampa tutti i documenti
    print(get_users())
    
    return render_template('index.html')

@app.route('/create_database')
def create_database():
    
    # Specifica il percorso del file CSV
    CSV_FILE_PATH = 'csv_prime_user/amazon_prime_users.csv'
     
    return load_csv_to_mongo(CSV_FILE_PATH)