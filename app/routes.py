from flask import Flask, render_template
from app import app


@app.route('/prova')
def index():
    return render_template('index.html')