from flask import Flask, render_template, request, flash, redirect, url_for, jsonify,session
import os
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import pymysql
from db import get_connection
import random

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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


with app.app_context():
    db.create_all()

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

@app.route('/audience_signup', methods=['POST'])
def audience_signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    day = int(request.form['day'])
    month = int(request.form['month'])
    year = int(request.form['year'])
    gender = request.form['gender']
    conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Bhavikgarg@30',  # Plain text, no URL encoding
            database='SharkTank6',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
    )
    cursor=conn.cursor()
    cursor3=conn.cursor()
    query="select count(*) as count from Audience"
    cursor3.execute(query)
    user_id=cursor3.fetchone()['count']+3
    cursor2 = conn.cursor()
    query2 = """
        INSERT INTO Audience (
            UserId, FirstName, LastName, Phone_Num, 
            Day_DOB, Month_DOB, Year_DOB, Gender
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor2.execute(query2,(user_id,first_name,last_name,phone,day,month,year,gender))

    query3 = "SELECT * FROM Audience WHERE FirstName = %s "
    cursor2.execute(query3, (first_name))
    audience = cursor2.fetchone()
    session['audienceId'] = audience['UserId']
    conn.commit() 
    cursor.close()
    return redirect(url_for('home1'))

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
    if email.endswith('@gmail.com'):
     username = email[:-10]  # Removes the last 10 characters: '@gmail.com'
    else:
        flash('Invalid email or password!', 'error')
        return render_template('login.html')
     
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
        query = "SELECT * FROM Audience inner join Pitcher on Audience.UserId=Pitcher.PitcherID WHERE FirstName = %s "
        cursor.execute(query, (username))
        pitcher = cursor.fetchone()
        if pitcher:
            session['pitcher_id'] = pitcher['PitcherID']
            return render_template('dash.html', pitcher=pitcher)
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
    


@app.route('/finalized_pitches')
def finalized_pitches():
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

        query = """
SELECT 
    p.PitchID AS Id,
    a.FirstName AS PitcherName,
    p.Title As title,
    p.EquityOffered As equity_offered,
    p.Valuation,
    p.Description
FROM 
    Pitch p
JOIN 
    PitchesProposedByPitcher pp ON pp.PitchID = p.PitchID
JOIN 
    Pitcher pi ON pi.PitcherID = pp.PitcherID
JOIN 
    Audience a ON a.UserId = pi.PitcherID;
        """

        cursor.execute(query)
        pitches = cursor.fetchall()

        return jsonify({'pitches': pitches})

    except Exception as e:
        print(f"Error fetching finalized pitches: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@app.route('/investor_login', methods=['POST'])
def investor_login():
    email = request.form['email']
     
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
        query = "SELECT * FROM Audience inner join Investor on Audience.UserId=Investor.InvestorID WHERE Email = %s "
        cursor.execute(query, (email))
        investor = cursor.fetchone()
        if investor:
            session['investorId'] = investor['InvestorID']
            return render_template('HomePageI.html', investor=investor)# change made by ansh
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
    

@app.route('/audience_login', methods=['POST'])
def audience_login():
    email = request.form['email']
    if email.endswith('@gmail.com'):
     username = email[:-10]  # Removes the last 10 characters: '@gmail.com'
    else:
        flash('Invalid email or password!', 'error')
        return render_template('login.html')
     
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
        query = "SELECT * FROM Audience WHERE FirstName = %s "
        cursor.execute(query, (username))
        audience = cursor.fetchone()
        if audience:
            session['audienceId'] = audience['UserId']
            return redirect(url_for('home1'))
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
    

@app.route('/admin_dashboard')
def admin_dashboard():
    # Fetch these values from the database
    conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Bhavikgarg@30',  # Plain text, no URL encoding
            database='SharkTank6',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
    )
    cursor = conn.cursor()
    cursor2=conn.cursor()
    cursor3=conn.cursor()
    query = "Select count(*) as count from Audience"
    query2= "Select count(*) as count from Audience where Is_Authenticated=0"
    query3="Select count(*) as count from Deals"
    cursor.execute(query)
    cursor2.execute(query2)
    cursor3.execute(query3)
    total_users = cursor.fetchone()['count']
    pending_verifications = cursor2.fetchone()['count']
    finalized_deals = cursor3.fetchone()['count']
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
        query="""
            SELECT 
                CONCAT(ai.FirstName) AS investor,
                CONCAT(ap.FirstName) AS pitcher,
                prop.Description AS valuation,
                'Finalized' AS status
            FROM Deals d
            JOIN ProposalForPitchByInvestor prop ON d.Proposal_of_Deal = prop.Proposal
            JOIN Investor i ON prop.InvestorID = i.InvestorID
            JOIN Pitcher pit ON prop.PitcherID = pit.PitcherID
            JOIN Audience ai ON i.InvestorID = ai.UserId
            JOIN Audience ap ON pit.PitcherID = ap.UserId
            JOIN Pitch p ON prop.PitchID = p.PitchID;
        """
        if filter_status != 'All':
            query += " WHERE d.Status = %s"
            cursor.execute(query, (filter_status,))
        else:
            cursor.execute(query)

        deals = cursor.fetchall()
        print(f"Fetched {len(deals)} deals from DB (filter: {filter_status})")  # Debug
        return jsonify({'deals': deals})

    except Exception as e:
        print(f"Error fetching deals: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()


@app.route('/logout')
def logout():
    # Add logout functionality here
    return redirect('/login')

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
            password='Bhavikgarg@30',
            database='SharkTank6',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor2 = conn.cursor()

        if is_verified:
            cursor.execute("""
                UPDATE Audience 
                SET Is_Authenticated = 1 
                WHERE UserId = %s
            """, (user_id,))

            cursor2.execute("""
                INSERT INTO Pitcher (PitcherID, Domain)
                SELECT UserId, 'Ai based techs are mainly area of interest'
                FROM Audience
                WHERE UserId = %s
                  AND Is_Authenticated = TRUE 
                  AND UserId NOT IN (SELECT PitcherID FROM Pitcher) 
                  AND UserId NOT IN (SELECT InvestorID FROM Investor)
            """, (user_id,))
            
            message = f"User {user_id} verified successfully"

        else:
            # Optional: If you want to mark rejected users or delete, add logic here
            message = f"User {user_id} rejected successfully"

        conn.commit()  # Commit in both cases

        # Check if user was actually updated
        affected_rows = cursor.rowcount
        if affected_rows == 0:
            return jsonify({'status': 'error', 'message': 'User not found or already processed'}), 404

        return jsonify({'status': 'success', 'message': message}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if 'conn' in locals() and conn:
            conn.close()

# Fetch top 10 trending pitches
def fetch_top_10_trending_pitches():
    query = "SELECT * FROM Pitch ORDER BY PopularityScore DESC LIMIT 10"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching top trending pitches: {e}")
        return []

# Fetch all pitches with sorting and search
def fetch_all_pitches(sort_by, search_query=None):
    query = "SELECT * FROM Pitch"
    filters = []

    if search_query:
        query += " WHERE Title LIKE %s OR Description LIKE %s"
        filters.extend([f"%{search_query}%", f"%{search_query}%"])

    if sort_by == 'newest':
        query += " ORDER BY DateOfPost DESC"
    elif sort_by == 'oldest':
        query += " ORDER BY DateOfPost ASC"
    elif sort_by == 'highest_engagement':
        query += " ORDER BY PopularityScore DESC"
    elif sort_by == 'lowest_valuation':
        query += " ORDER BY Valuation ASC"
    elif sort_by == 'highest_valuation':
        query += " ORDER BY Valuation DESC"
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, filters)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching pitches: {e}")
        return []

# 🆕 API to handle like (increment popularity score)
@app.route('/like_pitch/<int:pitch_id>', methods=['POST'])
def like_pitch(pitch_id):
    update_query = "UPDATE Pitch SET PopularityScore = PopularityScore + 1 WHERE PitchID = %s"
    fetch_query = "SELECT PopularityScore FROM Pitch WHERE PitchID = %s"
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(update_query, (pitch_id,))
                conn.commit()  # Commit the changes to the database
                cursor.execute(fetch_query, (pitch_id,))
                updated_score = cursor.fetchone()[0]  # Get the updated score
        return jsonify({"updated_score": updated_score})  # Send the updated score back to the frontend
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/index')
def home1():
    trending_ideas = fetch_top_10_trending_pitches()
    recent_pitches = trending_ideas[:4] if len(trending_ideas) >= 2 else trending_ideas
    print(len(recent_pitches))
    return render_template('index.html', all_pitches=recent_pitches, trending_ideas=trending_ideas[:4])

@app.route('/all_pitches')
def all_pitches_view():
    sort_by = request.args.get('sort_by', default='newest')
    search_query = request.args.get('search_query', default=None)
    all_pitches = fetch_all_pitches(sort_by, search_query)
    return render_template('all_pitches.html', all_pitches=all_pitches, sort_by=sort_by, search_query=search_query)


@app.route('/trending')
def trending():
    trending_ideas = fetch_top_10_trending_pitches()
    return render_template('trending.html', trending_ideas=trending_ideas)

@app.route('/request_pitcher')
def request_pitcher():
    return render_template('request_pitcher.html')

def get_user_profile(user_id):
    query = "SELECT UserID, FirstName, Phone_Num, Gender, Is_Authenticated FROM Audience WHERE UserID = %s"
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "UserID": row[0],
                        "Name": row[1],
                        "PhoneNumber": row[2],
                        "Gender": row[3],
                        "Age": random.randint(18, 45),
                        "AuthStatus": row[4]
                    }
    except Exception as e:
        print(f"Error fetching user profile: {e}")
    return None

@app.route('/profile')
def profile():
    user_id = session.get('audienceId')  
    print(user_id)
    if not user_id:
        print("hello1")
        return redirect(url_for('home1'))
    user_profile = get_user_profile(user_id)
    if not user_profile:
        return "User not found", 404

    return render_template('profile.html', audience=user_profile)

@app.route('/logout4')
def logout_for_audience():
    session.clear()  # This clears all session data
    return redirect(url_for('login')) 


@app.route('/faq')
def faq():
    return render_template('faq.html')


##START OF INVESTOR

@app.route('/start_inv')#change 1
def StartInv():#change 2
    return render_template('HomePageI.html')

@app.route('/ViewPitch')
def ViewPitch():
    return render_template('ViewPitchandAddPropI.html')

@app.route('/addProposal')
def AddProposal():
    return render_template('addPropoI.html')

@app.route('/ViewDeals')
def ViewAllDeals():
    return render_template('Acc_Deals_I.html')

@app.route('/backToHome')
def BackHome():
    return render_template('HomePageI.html')

@app.route('/backToView')
def BackViewPitch():
    return render_template('ViewPitchandAddPropI.html')

@app.route('/viewProfile')
def ViewProfile():
    return render_template('Profile_I.html')

@app.route('/InvestorLogout')
def InvestorLogout():
    return render_template('login.html')

@app.route('/pitchDisp')
def pitchDisp():

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    t1.pitchid,
                    t1.equityoffered,
                    t1.popularityscore,
                    t1.valuation,
                    t1.description,
                    t2.pitcherid
                FROM pitch t1, pitchesproposedbypitcher t2
                WHERE t1.pitchid = t2.pitchid;
            """
            cursor.execute(query)
            pitch_data = cursor.fetchall()

            # Calculate money demanded
            for pitch in pitch_data:
                pitch['moneydemanded'] = round((pitch['equityoffered'] * pitch['valuation']) / 100)

        return render_template('ViewPitchandAddPropI.html', pitches=pitch_data)
    except Exception as e:
        print("Error:", e)
        return "Something went wrong!"

@app.route('/submit_proposal', methods=['POST'])
def submit_proposal():
    pitch_id = request.form['pitchId']
    pitcher_id = request.form['pitcherId']
    investor_id = request.form['investorId']
    description = request.form['description']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO ProposalForPitchByInvestor (PitcherID, Description, InvestorID, PitchID)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (pitcher_id, description, investor_id, pitch_id))
        conn.commit()

        flash("Proposal submitted successfully!", "success")
        return redirect(url_for('StartInv'))#change3

    except Exception as e:
        print("Error inserting proposal:", e)
        flash("Error submitting proposal. Try again.", "error")
        return redirect(url_for('StartInv'))#change4

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/dispDeal')
def dispDeal():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT proposalforpitchbyinvestor.proposal AS proposalid,
                       proposalforpitchbyinvestor.pitcherid,
                       proposalforpitchbyinvestor.description,
                       proposalforpitchbyinvestor.investorid,
                       proposalforpitchbyinvestor.pitchid
                FROM proposalforpitchbyinvestor, deals
                WHERE proposalforpitchbyinvestor.proposal = deals.proposal_of_deal;
            """
            cursor.execute(query)
            records = cursor.fetchall()
    finally:
        connection.close()
    return render_template('Acc_Deals_I.html', deals=records)

if __name__ == '__main__':
    app.run(debug=True, port=5001)



