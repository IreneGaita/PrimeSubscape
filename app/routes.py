from datetime import datetime
from bson import ObjectId
from flask import jsonify, render_template, request, redirect, url_for
from flask import current_app as app
from app.models import add_user,search_user, delete_user, search_all_user, edit_user, find_user_by_id, show_end_date
from app.database_init import load_csv_to_mongo


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user_route(user_id):
    if request.method == 'POST':
        # Aggiorna i dettagli dell'utente nel database
        user_data = {
        "Name": request.form['name'],
        "Email Address": request.form['email'],
        "Username": request.form['username'],
        "Date of Birth": datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
        "Gender": request.form['gender'],
        "Location": request.form['location'],
        "Subscription": {
            "Start Date": datetime.strptime(request.form['subscription_start_date'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
            "End Date": datetime.strptime(request.form['subscription_end_date'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
            "Plan": request.form['subscription_plan'],
            "Payment Information": request.form['payment_information'],
            "Renewal Status": request.form['renewal_status']
        },
        "Usage": {
            "Frequency": int(request.form['usage_frequency']),
            "Purchase History": request.form.getlist('purchase_history'),
            "Favorite Genres": request.form.getlist('favorite_genres'),
            "Devices Used": request.form.getlist('devices_used'),
            "Engagement Metrics": request.form['engagement_metrics']
        },
        "Feedback": {
            "Ratings": float(request.form['ratings']),
            "Customer Support Interactions": int(request.form['customer_support_interactions'])
        }
        }
        
        edit_user(user_data, user_id)
        return redirect(url_for('edit_user_route', user_id=user_id))
    
    # Recupera i dettagli dell'utente dal database
    user = find_user_by_id(user_id)

    #adapt date format
    if user['Date of Birth'] is type(str):
        user['Date of Birth'] = datetime.strptime(user['Date of Birth'], '%Y-%m-%d').date().strftime('%Y-%m-%d')
        user['Subscription']['Start Date'] = datetime.strptime(user['Subscription']['Start Date'], '%Y-%m-%d').date().strftime('%Y-%m-%d')
        user['Subscription']['End Date'] = datetime.strptime(user['Subscription']['End Date'], '%Y-%m-%d').date().strftime('%Y-%m-%d')
    else:
        user["Date of Birth"] = user["Date of Birth"].strftime('%Y-%m-%d')
        user["Subscription"]["Start Date"] = user["Subscription"]["Start Date"].strftime('%Y-%m-%d')
        user["Subscription"]["End Date"] = user["Subscription"]["End Date"].strftime('%Y-%m-%d')

    return render_template('edit_user.html', user=user)
        

@app.route('/add_user', methods=['POST'])
def add_user_route():
    user_data = {
        "Name": request.form['name'],
        "Email Address": request.form['email'],
        "Username": request.form['username'],
        "Date of Birth": datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
        "Gender": request.form['gender'],
        "Location": request.form['location'],
        "Subscription": {
            "Start Date": datetime.strptime(request.form['subscription_start_date'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
            "End Date": datetime.strptime(request.form['subscription_end_date'], '%Y-%m-%d').date().strftime('%Y-%m-%d'),
            "Plan": request.form['subscription_plan'],
            "Payment Information": request.form['payment_information'],
            "Renewal Status": request.form['renewal_status']
        },
        "Usage": {
            "Frequency": int(request.form['usage_frequency']),
            "Purchase History": request.form.getlist('purchase_history'),
            "Favorite Genres": request.form.getlist('favorite_genres'),
            "Devices Used": request.form.getlist('devices_used'),
            "Engagement Metrics": request.form['engagement_metrics']
        },
        "Feedback": {
            "Ratings": float(request.form['ratings']),
            "Customer Support Interactions": int(request.form['customer_support_interactions'])
        }
    }
    
    # Inserisci il nuovo documento nel database
    result = add_user(user_data)
    
    return jsonify({"message": "User added successfully", "id": str(result.inserted_id)}), 201

@app.route('/create_database')
def create_database():
    
    # Specifica il percorso del file CSV
    CSV_FILE_PATH = 'csv_prime_user/amazon_prime_users.csv'
     
    return load_csv_to_mongo(CSV_FILE_PATH)

@app.route('/find_user', methods=['GET','POST'])
def find_user():
    if request.method == 'POST':
        nome = request.form.get('Name')
        find_user = search_user(nome)
        return render_template('querytemplate.html', find_user=find_user)
    else:
        return render_template('index.html', find_user=[])
    

@app.route('/delete_user', methods=['POST'])
def delete_user_route():
    #get the json data
    data = request.get_json()
    print("I am here")
    user_id = data['userId']

    result = delete_user(user_id)
    print("User deleted successfully!")
    return result

@app.route('/show_all_users', methods=['GET'])
def show_all_users():
    users = search_all_user()
    return render_template('querytemplate.html', find_user=users)


@app.route('/show_end_date', methods=['GET'])
def show_end_date_route():
    expired_users = show_end_date()  
    return render_template('querytemplate.html', expired_users=expired_users)
