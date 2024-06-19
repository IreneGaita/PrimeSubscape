from flask import render_template, request
from flask import current_app as app
from app.models import add_user
from app.database_init import load_csv_to_mongo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def prova_db():
    nome = request.form.get('nome')
    email = request.form.get('email')
    password = request.form.get('password')
    
    add_user(nome, email, password)
    
    return "utente aggiunto con successo"

@app.route('/create_database')
def create_database():
    
    # Specifica il percorso del file CSV
    CSV_FILE_PATH = 'csv_prime_user/amazon_prime_users.csv'
     
    return load_csv_to_mongo(CSV_FILE_PATH)