from datetime import datetime
from bson import ObjectId
from flask import jsonify, render_template, request, redirect, url_for
from flask import current_app as app
from app.models import add_user, aggregate_subscription_years, count_devices_used, count_plans, count_renewal_status, find_every_user_less_greater_equal_subscription_years, find_users_with_favorite_genres, find_users_with_one_device, get_unique_genres, intervall_date, rating_by_location,search_user, delete_user, search_all_user, edit_user, find_user_by_id, show_end_date, show_gender, show_location, show_ratings_lower, user_monthly_plan_frequency
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
            "Date of Birth": datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d'),
            "Gender": request.form['gender'],
            "Location": request.form['location'],
            "Subscription": {
                "Start Date": datetime.strptime(request.form['subscription_start_date'], '%Y-%m-%d'),
                "End Date": datetime.strptime(request.form['subscription_end_date'], '%Y-%m-%d'),
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

    # Adatta il formato delle date
    if isinstance(user['Date of Birth'], str):
        user['Date of Birth'] = datetime.strptime(user['Date of Birth'], '%Y-%m-%d').strftime('%Y-%m-%d')
        user['Subscription']['Start Date'] = datetime.strptime(user['Subscription']['Start Date'], '%Y-%m-%d').strftime('%Y-%m-%d')
        user['Subscription']['End Date'] = datetime.strptime(user['Subscription']['End Date'], '%Y-%m-%d').strftime('%Y-%m-%d')
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
        "Date of Birth": datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d'),
        "Gender": request.form['gender'],
        "Location": request.form['location'],
        "Subscription": {
            "Start Date": datetime.strptime(request.form['subscription_start_date'], '%Y-%m-%d'),
            "End Date": datetime.strptime(request.form['subscription_end_date'], '%Y-%m-%d'),
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
    user = show_end_date()  
    return render_template('showexpiredusers.html', users=user)


@app.route('/intervall_date', methods=['POST'])
def interval_date_route():
    startDate = request.form.get('Start Date')
    startDate = datetime.strptime(startDate, '%Y-%m-%d')
    endDate = request.form.get('End Date')
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    user = intervall_date(startDate,endDate)  
    return render_template('querytemplate.html', find_user=user)

@app.route('/show_gender', methods=['POST'])
def show_gender_route():
    gender = request.form.get('Gender')
    user= show_gender(gender)  
    return render_template('querytemplate.html', find_user=user)

@app.route('/show_location', methods=['POST'])
def show_location_route():
    location = request.form.get('Location')
    user= show_location(location)  
    return render_template('querytemplate.html', find_user=user)

@app.route('/show_ratings_lower', methods=['POST'])
def show_ratings_lower_route():
    rating = float(request.form.get('Ratings'))
    interactionsupp= float(request.form.get('Customer Support Interactions'))
    user=show_ratings_lower(rating,interactionsupp)  
    return render_template('querytemplate.html', find_user=user)

@app.route('/count_plans', methods=['POST'])
def count_plans_route():
    plans = count_plans()
    return render_template('index.html', plans=plans)

@app.route('/rating_by_location',methods=['POST'])
def average_rating_by_location_route():
    avg_ratings = rating_by_location()
    return render_template('index.html', avg_ratings=avg_ratings)

@app.route('/users_with_one_device', methods=['GET'])
def users_with_one_device_route():
    user = find_users_with_one_device()
    return render_template('querytemplate.html', find_user=user)

@app.route('/users_with_monthly_plan', methods=['GET'])
def user_monthly_plan_frequency_route():
    user = user_monthly_plan_frequency()
    return render_template('querytemplate.html', find_user=user)

@app.route('/renewal_status_counts', methods=['POST'])
def renewal_status_counts_route():
    counts = count_renewal_status()
    return render_template('index.html', counts=counts)


@app.route('/select_genres', methods=['GET', 'POST'])
def select_genres():
    if request.method == 'POST':
        selected_genres = request.form.getlist('genres')
        users = find_users_with_favorite_genres(selected_genres)
        return render_template('querytemplate.html', find_user=users, genres=get_unique_genres(), selected_genres=selected_genres)
    else:
        genres = get_unique_genres()
        return render_template('querytemplate.html', genres=genres, find_user=[], selected_genres=[])

@app.route('/count_devices_used', methods=['POST'])
def count_devices_used_route():
    device_counts = count_devices_used()
    return render_template('index.html', device_counts=device_counts)

@app.route("/get_all_subscriptions_years", methods=["GET"])
def get_subscription_years():
    # Recupera i dati aggregati per gli anni di sottoscrizione
    users= aggregate_subscription_years()
    #gli anni sono espressi da 0 a 1, convertili in mesi
    for user in users:
        
        user["Subscription"]["Years"] = (user["Subscription"]["Years"] * 12).__round__()
        
    return render_template("index.html", subscription_years=users)


@app.route('/search_user_by_subscription_months', methods=['POST'])
def search_user_by_subscription_months():
    months = int(request.form.get('months')) / 12
    operator = request.form.get('operator')
    users = find_every_user_less_greater_equal_subscription_years(operator, months)
    return render_template('querytemplate.html', find_user=users)