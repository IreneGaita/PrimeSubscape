from flask import Flask, render_template
from flask import current_app as app, render_template
from app.models import add_user, get_users
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