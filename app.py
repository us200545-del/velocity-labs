from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
from waitress import serve
import os
import json

app = Flask(__name__)
app.secret_key = 'velocity_labs_secret_key_2026'
CORS(app)

# --- USER DATABASE LOGIC ---
USER_DB = 'users.json'

def get_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, 'w') as f:
            json.dump([], f)
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f)

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uid = request.form.get('username')
        pwd = request.form.get('password')
        recovery = request.form.get('recovery_code')
        
        users = get_users()
        if any(u['username'] == uid for u in users):
            return "Driver ID already exists. <a href='/signup'>Try another</a>"
        
        users.append({"username": uid, "password": pwd, "recovery": recovery})
        save_users(users)
        return redirect(url_for('login'))
    return render_template('auth/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uid = request.form.get('username')
        pwd = request.form.get('password')
        
        # Hardcoded admin check + Database check
        users = get_users()
        user_match = next((u for u in users if u['username'] == uid and u['password'] == pwd), None)
        
        if (uid == 'admin' and pwd == 'velocity2026') or user_match:
            session['logged_in'] = True
            session['username'] = uid
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials. <a href='/login'>Try again</a>"
    return render_template('auth/login.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        uid = request.form.get('username')
        recovery = request.form.get('recovery_code')
        new_pwd = request.form.get('new_password')
        
        users = get_users()
        for u in users:
            if u['username'] == uid and u['recovery'] == recovery:
                u['password'] = new_pwd
                save_users(users)
                return "Passkey Updated. <a href='/login'>Login</a>"
        return "Identity Verification Failed."
    # Make sure you have created templates/auth/reset.html
    return render_template('auth/reset.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/inventory/<category>')
def inventory(category):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    part_data = {
        "alloys": {
            "title": "Forged Alloy Selection",
            "items": [
                {"name": "BBS RI-D Magnesium", "img": "bbs_rid.jpg", "price": "₹4,50,000", "compat": "BMW M4, Porsche 911, Audi A7"},
                {"name": "HRE P101 SC", "img": "hre_p101.jpg", "price": "₹5,20,000", "compat": "Mercedes CLS, Porsche 911"},
                {"name": "Vossen S17-01", "img": "vossen_s17.jpg", "price": "₹3,80,000", "compat": "BMW M4, Virtus GT, Baleno RS"}
            ]
        },
        "exhaust": {
            "title": "Performance Exhaust Systems",
            "items": [
                {"name": "Akrapovič Titanium", "img": "akrapovic.jpg", "price": "₹2,80,000", "compat": "BMW M4, Porsche 911"},
                {"name": "IPE Valvetronic", "img": "ipe.jpg", "price": "₹1,95,000", "compat": "Mercedes CLS, Nissan GTR"},
                {"name": "Armytrix Cat-Back", "img": "armytrix.jpg", "price": "₹2,15,000", "compat": "BMW M4, Audi A7"}
            ]
        },
        "turbo": {
            "title": "Turbochargers",
            "items": [
                {"name": "Garrett G-Series", "img": "garrett.jpg", "price": "₹2,45,000", "compat": "Universal / Custom Builds"},
                {"name": "Pure Turbos S58", "img": "pure_turbo.jpg", "price": "₹4,10,000", "compat": "BMW M4 Competition"}
            ]
        },
        "suspension": {
            "title": "Suspension",
            "items": [
                {"name": "AirLift Performance 3H", "img": "airlift.jpg", "price": "₹3,40,000", "compat": "All Models (Air-Ride)"},
                {"name": "KW V3 Coilovers", "img": "kw_v3.jpg", "price": "₹1,85,000", "compat": "BMW M4, Porsche 911, Audi A7"}
            ]
        },
        "filter": {
            "title": "Air Filters",
            "items": [
                {"name": "Eventuri Carbon", "img": "eventuri.jpg", "price": "₹85,000", "compat": "BMW M4, Audi A7"},
                {"name": "K&N Typhoon", "img": "kn_filter.jpg", "price": "₹18,500", "compat": "Virtus GT, Baleno RS"}
            ]
        },
        "spoilers": {
            "title": "Aero Parts",
            "items": [
                {"name": "Vorsteiner Wing", "img": "vorsteiner.jpg", "price": "₹1,15,000", "compat": "Porsche 911, BMW M4"},
                {"name": "ADRO Front Lip", "img": "adro.jpg", "price": "₹55,000", "compat": "BMW M4, Nissan GTR"}
            ]
        },
        "headlights": {
            "title": "Lighting",
            "items": [
                {"name": "BMW Laserlight", "img": "laserlight.jpg", "price": "₹1,40,000", "compat": "BMW M4 (G82/G80)"},
                {"name": "OLED Taillights", "img": "oled.jpg", "price": "₹88,000", "compat": "BMW M4, Audi A7"}
            ]
        }
    }

    data = part_data.get(category)
    if data:
        return render_template('stock.html', title=data['title'], items=data['items'])
    return redirect(url_for('home'))

@app.route('/view-build')
def view_build():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('cart.html')

@app.route('/payment')
def payment():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('payment.html')

if __name__ == '__main__':
    # For Render/Production, use the environment PORT
    port = int(os.environ.get('PORT', 5000))
    print(f"📡 ACCESS LINK: http://127.0.0.1:{port}")
    serve(app, host='0.0.0.0', port=port)