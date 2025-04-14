from flask import Flask, render_template, request, flash, redirect, url_for, jsonify,session
import os
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import pymysql

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bhavikgarg%4030@localhost:3306/SharkTank6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

# DB
db = SQLAlchemy(app)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bhavikgarg%4030',
    'database': 'SharkTank6'
}
def get_db_connection():
    return pymysql.connect(**db_config)
# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# Create tables inside app context
with app.app_context():
    db.create_all()
# Mock databases
pitches_db = [
    {'id': 1, 'pitcher': 'Pitcher 1', 'title': 'Pitch 1', 'status': 'Pending'},
    {'id': 2, 'pitcher': 'Pitcher 2', 'title': 'Pitch 2', 'status': 'Pending'},
    {'id': 3, 'pitcher': 'Pitcher 3', 'title': 'Pitch 3', 'status': 'Pending'}
]

deals_db = [
    {"id": 1, "investor": "Investor 1", "pitcher": "Pitcher 1", "status": "Pending"},
    {"id": 2, "investor": "Investor 2", "pitcher": "Pitcher 2", "status": "Approved"},
    {"id": 3, "investor": "Investor 3", "pitcher": "Pitcher 3", "status": "Rejected"},
]

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Bhavikgarg30',
        database='SharkTank6',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('lyrics.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['password']
    
    conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Bhavikgarg@30',  # Plain text, no URL encoding
            database='SharkTank6',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
    )
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM Admin WHERE Email = %s AND Password_ = %s"
        cursor.execute(query, (email, password))
        admin = cursor.fetchone()

        if admin:
            session['admin_id'] = admin['UserId']
            session['admin_email'] = admin['Email']
            return render_template('Admin.html', admin=admin)
        else:
            flash('Invalid email or password!', 'error')
            return render_template('login.html')

    except mysql.connector.Error as err:
        print("Database error:", err)
        flash('Something went wrong. Please try again later.', 'error')
        return render_template('login.html')

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.route('/pitcher_login', methods=['POST'])
def pitcher_login():
    email = request.form['email']
    password = request.form['password']
    # Process the login for pitcher
    return f"Pitcher logged in with email {email}"

@app.route('/investor_login', methods=['POST'])
def investor_login():
    email = request.form['email']
    password = request.form['password']
    # Process the login for investor
    return f"Investor logged in with email {email}"

@app.route('/audience_login', methods=['POST'])
def audience_login():
    email = request.form['email']
    password = request.form['password']
    # Process the login for audience
    return f"Audience logged in with email {email}"

@app.route('/admin_dashboard')
def admin_dashboard():
    # Fetch these values from the database
    total_users = 24521
    pending_verifications = 156
    finalized_deals = 89

    return render_template('Admin.html', 
                          total_users=total_users,
                          pending_verifications=pending_verifications,
                          finalized_deals=finalized_deals)

@app.route('/user_management')
def user_management():
    return render_template('UserManagement.html')

@app.route('/pitch_verification')
def pitch_verification():
    return render_template('PitchVerification.html')

@app.route('/monitor_deals_page')
def monitor_deals_page():
    print("Attempting to render:", app.template_folder + '/MonitorDeals.html')
    return render_template('MonitorDeals.html')


@app.route('/monitor_deals')
def monitor_deals():
    filter_status = request.args.get('filter', 'All')
    filtered_deals = [d for d in deals_db if filter_status == 'All' or d['status'] == filter_status]
    print(f"Sending {len(filtered_deals)} deals (filter: {filter_status})")  # Debug
    return jsonify({'deals': filtered_deals})


@app.route('/logout')
def logout():
    # Add logout functionality here
    return redirect('/login')


@app.route('/pitches_to_verify')
def pitches_to_verify():
    filter_status = request.args.get('filter', 'All')
    
    filtered_pitches = pitches_db
    if filter_status != 'All':
        filtered_pitches = [p for p in pitches_db if p['status'] == filter_status]
    
    print(f"Returning {len(filtered_pitches)} pitches with filter: {filter_status}")  # Debug print
    return jsonify({
        'pitches': filtered_pitches,
        'message': 'Success',
        'status': 200
    })

@app.route('/approve_pitch', methods=['POST'])
def approve_pitch():
    data = request.get_json()
    pitch_id = data.get('id')
    
    # Update pitch status in database
    for pitch in pitches_db:
        if pitch['id'] == pitch_id:
            pitch['status'] = 'Approved'
            break
    
    return jsonify({'status': 'success', 'message': f'Pitch {pitch_id} approved'})

@app.route('/reject_pitch', methods=['POST'])
def reject_pitch():
    data = request.get_json()
    pitch_id = data.get('id')
    
    # Update pitch status in database
    for pitch in pitches_db:
        if pitch['id'] == pitch_id:
            pitch['status'] = 'Rejected'
            break
    
    return jsonify({'status': 'success', 'message': f'Pitch {pitch_id} rejected'})

@app.route('/approve_deal', methods=['POST'])
def approve_deal():
    try:
        data = request.get_json()
        deal_id = data.get('deal_id')
        
        # Find and update deal
        for deal in deals_db:
            if deal['id'] == deal_id:
                deal['status'] = 'Approved'
                print(f"Deal {deal_id} approved")  # Debug
                return jsonify({
                    'status': 'success', 
                    'message': f'Deal {deal_id} approved'
                })
        
        return jsonify({
            'status': 'error',
            'message': 'Deal not found'
        }), 404
        
    except Exception as e:
        print(f"Error approving deal: {str(e)}")  # Debug
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/reject_deal', methods=['POST'])
def reject_deal():
    try:
        data = request.get_json()
        deal_id = data.get('deal_id')
        
        # Find and update deal
        for deal in deals_db:
            if deal['id'] == deal_id:
                deal['status'] = 'Rejected'
                print(f"Deal {deal_id} rejected")  # Debug
                return jsonify({
                    'status': 'success', 
                    'message': f'Deal {deal_id} rejected'
                })
        
        return jsonify({
            'status': 'error',
            'message': 'Deal not found'
        }), 404
        
    except Exception as e:
        print(f"Error rejecting deal: {str(e)}")  # Debug
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/pending_users')
def get_pending_users():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Bhavikgarg@30',  # Plain text, no URL encoding
            database='SharkTank6',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
        )
        cursor = conn.cursor()
        cursor.execute("""
                SELECT 
                    UserId as id,
                    CONCAT(FirstName, ' ', IFNULL(LastName, '')) as name,
                    Phone_Num as phone,
                    CONCAT(Day_DOB, '/', Month_DOB, '/', Year_DOB) as dob,
                    Gender,
                    Is_Authenticated
                FROM Audience 
                WHERE Is_Authenticated = 0
            """)
        users = cursor.fetchall()
        return jsonify({'pending_users': users, 'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/verify_user', methods=['POST'])
def verify_user():
    return update_user_status(request.json.get('user_id'), True)

@app.route('/reject_user', methods=['POST'])
def reject_user():
    return update_user_status(request.json.get('user_id'), False)

def update_user_status(user_id, is_verified):
    if not user_id:
        return jsonify({'status': 'error', 'message': 'User ID required'}), 400
    
    try:
            conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Bhavikgarg@30',  # Plain text, no URL encoding
            database='SharkTank6',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
           )
            cursor = conn.cursor()
        
            if is_verified:
                cursor.execute("""
                    UPDATE Audience 
                    SET Is_Authenticated = 1 
                    WHERE UserId = %s
                """, (user_id,))
                message = f"User {user_id} verified successfully"
            else:
                cursor.execute("""
                    DELETE FROM Audience 
                    WHERE UserId = %s AND Is_Authenticated = 0
                """, (user_id,))
                message = f"User {user_id} rejected successfully"
            
            conn.commit()
            affected_rows = cursor.rowcount
            
            if affected_rows == 0:
                return jsonify({'status': 'error', 'message': 'User not found or already processed'}), 404
            
            return jsonify({'status': 'success', 'message': message})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)


########################################################################################################

