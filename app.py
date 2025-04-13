from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

pending_users_db = [
    {'id': 1, 'name': 'User 1', 'role': 'Investor', 'status': 'pending'},
    {'id': 2, 'name': 'User 2', 'role': 'Pitcher', 'status': 'pending'},
    {'id': 3, 'name': 'User 3', 'role': 'Audience', 'status': 'pending'}
]

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
    # Process the login for admin
    if email == 'bhavik@gmail.com':
        return render_template('Admin.html')
    else:
        flash('Invalid email or password!', 'error')
        return render_template('login.html')

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
    pending_users = [user for user in pending_users_db if user['status'] == 'pending']
    print("Current pending users:", pending_users)  # Debug print
    return jsonify({'pending_users': pending_users})

@app.route('/verify_user', methods=['POST'])
def verify_user():
    data = request.get_json()
    user_id = data.get('user_id')
    
    # Update user status in our "database"
    for user in pending_users_db:
        if user['id'] == user_id:
            user['status'] = 'verified'
            break
    
    return jsonify({'status': 'success', 'message': f'User {user_id} verified'})

@app.route('/reject_user', methods=['POST'])
def reject_user():
    data = request.get_json()
    user_id = data.get('user_id')
    
    # Update user status in our "database"
    for user in pending_users_db:
        if user['id'] == user_id:
            user['status'] = 'rejected'
            break
    
    return jsonify({'status': 'success', 'message': f'User {user_id} rejected'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)