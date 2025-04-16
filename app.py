from flask import Flask, request, redirect, render_template, url_for, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Session ends when browser is closed
app.config['SESSION_PERMANENT'] = False

# MySQL setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kkav5603",
    database="travel_planner"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('user_name'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Save new user, no duplicate checks
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO user_details_one (name, email, phone, password) VALUES (%s, %s, %s, %s)",
            (name, email, phone, hashed_password)
        )
        db.commit()

        # Store session
        cursor.execute("SELECT * FROM user_details_one WHERE email = %s", (email,))
        user = cursor.fetchone()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('index'))

    return render_template('login.html')

# @app.route('/api/plan-trip', methods=['POST'])
# def plan_trip():
#     if 'user_id' not in session:
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.get_json()
#     budget = data['budget']
#     duration = data['duration']

#     query = "SELECT * FROM destinations WHERE cost <= %s AND duration <= %s"
#     cursor.execute(query, (budget, duration))
#     results = cursor.fetchall()
#     return jsonify(results)
@app.route('/api/plan-trip', methods=['POST'])
def plan_trip():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # Getting the input data from the request
    data = request.get_json()
    input_cost = data['budget']
    input_duration = data['duration']

    # Calculate the cost range (±2000)
    lower_bound_cost = input_cost - 2000
    upper_bound_cost = input_cost + 2000

    # Calculate the duration range (±2 days)
    lower_bound_duration = input_duration - 2
    upper_bound_duration = input_duration + 2

    # Query to get destinations within the cost and duration range
    query = "SELECT * FROM destinations WHERE cost BETWEEN %s AND %s AND duration BETWEEN %s AND %s"
    cursor.execute(query, (lower_bound_cost, upper_bound_cost, lower_bound_duration, upper_bound_duration))
    results = cursor.fetchall()

    return jsonify(results)



@app.route('/api/book', methods=['POST'])
def book_destination():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    destination_id = data.get('destination_id')
    user_name = data.get('user_name')
    mobile_number = data.get('mobile_number')

    if not all([destination_id, user_name, mobile_number]):
        return jsonify({"error": "Missing data"}), 400

    # Insert into bookings table
    cursor.execute(
        "INSERT INTO bookings (user_id, destination_id, user_name, mobile_number) VALUES (%s, %s, %s, %s)",
        (session['user_id'], destination_id, user_name, mobile_number)
    )
    db.commit()

    return jsonify({"message": "Booking successful"})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
