#FOR DISK 
# from dotenv import load_dotenv
# load_dotenv()
# import os
# from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
# import numpy as np
# import joblib
# import smtplib
# import sqlite3
# import bcrypt


# # ---------------- APP ----------------
# app = Flask(__name__)
# app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# # ---------------- ADMIN CONFIG ----------------
# ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
# ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# # ---------------- DATABASE ----------------
# def init_db():
#     os.makedirs("/data", exist_ok=True)  # ensure folder exists
    
#     conn = sqlite3.connect("/data/users.db")  
#     c = conn.cursor()
    
#     c.execute("""CREATE TABLE IF NOT EXISTS users(
#                  id INTEGER PRIMARY KEY AUTOINCREMENT,
#                  first_name TEXT,
#                  last_name TEXT,
#                  email TEXT UNIQUE,
#                  phone TEXT UNIQUE,
#                  password TEXT NOT NULL,
#                  dob TEXT,
#                  gender TEXT
#                  )""")
    
#     conn.commit()
#     conn.close()

# init_db()

# # ---------------- ML MODEL ----------------
# model = joblib.load("model/house_rent_rf_model.pkl")
# city_map = {"Bangalore":0,"Chennai":1,"Delhi":2,"Hyderabad":3,"Kolkata":4,"Mumbai":5}
# furnishing_map = {"Furnished":0,"Semi-Furnished":1,"Unfurnished":2}

# # ---------------- SIGNUP ----------------
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         first_name = request.form["first_name"]
#         last_name = request.form["last_name"]
#         email = request.form["email"]
#         phone = request.form["phone"]
#         password = request.form["password"].encode('utf-8')
#         dob = request.form["dob"]
#         gender = request.form["gender"]

#         hashed = bcrypt.hashpw(password, bcrypt.gensalt())

#         try:
#             conn = sqlite3.connect("/data/users.db")
#             c = conn.cursor()
#             c.execute("""INSERT INTO users (first_name, last_name, email, phone, password, dob, gender)
#                          VALUES (?,?,?,?,?,?,?)""",
#                       (first_name, last_name, email, phone, hashed, dob, gender))
#             conn.commit()
#             conn.close()

#             flash("Account created! Please login.", "success")
#             return redirect(url_for("login"))

#         except sqlite3.IntegrityError:
#             flash("Email or Phone already exists.", "danger")
#             return render_template("signup.html")

#     return render_template("signup.html")

# # ---------------- LOGIN ----------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("email") 
#         password = request.form.get("password").encode('utf-8')

#         conn = sqlite3.connect("/data/users.db")
#         c = conn.cursor()
#         c.execute("SELECT password,email FROM users WHERE email=? OR phone=?", (username, username))
#         row = c.fetchone()
#         conn.close()

#         if row:
#             stored_password = row[0]

#             # HANDLE BOTH CASES (bytes OR string)
#             if isinstance(stored_password, str):
#                 stored_password = stored_password.encode('utf-8')

#             if bcrypt.checkpw(password, stored_password):
#                 session.clear()
#                 session["user"] = row[1]
#                 return redirect(url_for("home"))

#         flash("Invalid credentials", "danger")
#         return render_template("login.html")

#     return render_template("login.html")

# # ---------------- ADMIN LOGIN ----------------
# @app.route("/admin", methods=["GET", "POST"])
# def admin():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")

#         if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
#             session.clear()
#             session["admin"] = True
#             return redirect(url_for("admin_dashboard"))
#         else:
#             flash("Wrong admin credentials", "danger")

#     return render_template("admin_login.html")

# # ---------------- ADMIN DASHBOARD ----------------
# @app.route("/admin/dashboard")
# def admin_dashboard():
#     if not session.get("admin"):
#         return redirect(url_for("admin"))
#     return render_template("admin_dashboard.html")

# # ---------------- DOWNLOAD DB ----------------
# @app.route("/download_db")
# def download_db():
#     if not session.get("admin"):
#         return "Unauthorized", 403
#     return send_file("/data/users.db", as_attachment=True)

# # ---------------- LOGOUT ----------------
# @app.route("/logout")
# def logout():
#     session.clear()
#     flash("You have been logged out.", "info")
#     return redirect(url_for("login"))

# # ---------------- HOME ----------------
# @app.route("/")
# def home():
#     if session.get("admin"):
#         return redirect(url_for("admin_dashboard"))

#     if "user" not in session:
#         return redirect(url_for("login"))

#     return render_template("index.html", user=session["user"])

# @app.route("/about")
# def about():
#     if "user" not in session:
#         return redirect(url_for("login"))
#     return render_template("about.html")

# # ---------------- PREDICT ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     if "user" not in session:
#         return redirect(url_for("login"))

#     try:
#         form_data = request.form.to_dict()   # ✅ FIX

#         bhk = int(form_data["bhk"])
#         size = float(form_data["size"])
#         floor = int(form_data["floor"])
#         city = city_map[form_data["city"]]
#         furnishing = furnishing_map[form_data["furnishing"]]
#         bathroom = int(form_data["bathroom"])

#         input_data = np.array([[bhk, size, floor, city, furnishing, bathroom]])
#         prediction = np.expm1(model.predict(input_data))[0]

#         return render_template("index.html",
#                                prediction=round(prediction),
#                                form_data=form_data)

#     except:
#         return render_template("index.html", prediction="Error", form_data={})

# # ---------------- CONTACT ----------------
# @app.route("/contact", methods=["POST"])
# def contact():
#     if "user" not in session:
#         return jsonify({"status":"fail","message":"Not logged in"})
#     try:
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']

#         # Email credentials from environment
#         sender_email = os.environ.get("EMAIL_USER")
#         receiver_email = os.environ.get("EMAIL_USER")
#         password = os.environ.get("EMAIL_PASS")

#         full_message = f"Subject: New Contact Message\n\nName: {name}\nEmail: {email}\nMessage: {message}"
#         server = smtplib.SMTP('smtp.gmail.com',587)
#         server.starttls()
#         server.login(sender_email,password)
#         server.sendmail(sender_email,receiver_email,full_message)
#         server.quit()
#         return jsonify({"status":"success"})
#     except Exception as e:
#         print(e)
#         return jsonify({"status":"fail"})

# # ---------------- RUN ----------------
# if __name__=="__main__":
#     app.run(debug=True)








# FOR DEPLOYMENT 
# ---------------- ENV ----------------
from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
import numpy as np
import joblib
import smtplib
import sqlite3
import bcrypt

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# ---------------- ADMIN ----------------
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# ---------------- DATABASE PATH ----------------
DB_PATH = "users.db"  

def get_db():
    return sqlite3.connect(DB_PATH, timeout=10)

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("PRAGMA journal_mode=WAL;")

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        phone TEXT UNIQUE,
        password BLOB,
        dob TEXT,
        gender TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- ML MODEL ----------------
model = joblib.load("model/house_rent_rf_model.pkl")

city_map = {"Bangalore":0,"Chennai":1,"Delhi":2,"Hyderabad":3,"Kolkata":4,"Mumbai":5}
furnishing_map = {"Furnished":0,"Semi-Furnished":1,"Unfurnished":2}

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            phone = request.form["phone"]
            password = request.form["password"].encode('utf-8')
            dob = request.form["dob"]
            gender = request.form["gender"]

            hashed = bcrypt.hashpw(password, bcrypt.gensalt())

            conn = get_db()
            c = conn.cursor()

            c.execute("""
            INSERT INTO users (first_name, last_name, email, phone, password, dob, gender)
            VALUES (?,?,?,?,?,?,?)
            """, (first_name, last_name, email, phone, hashed, dob, gender))

            conn.commit()
            conn.close()

            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Email or Phone already exists.", "danger")

        except Exception as e:
            print("Signup Error:", e)
            flash("Something went wrong!", "danger")

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("email")
            password = request.form.get("password").encode('utf-8')

            conn = get_db()
            c = conn.cursor()

            c.execute("SELECT password,email FROM users WHERE email=? OR phone=?", (username, username))
            row = c.fetchone()
            conn.close()

            if row:
                stored_password = row[0]

                if bcrypt.checkpw(password, stored_password):
                    session.clear()
                    session["user"] = row[1]
                    return redirect(url_for("home"))

            flash("Invalid credentials", "danger")

        except Exception as e:
            print("Login Error:", e)
            flash("Login error!", "danger")

    return render_template("login.html")

# ---------------- ADMIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Wrong admin credentials", "danger")

    return render_template("admin_login.html")

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    return render_template("admin_dashboard.html")

# ---------------- DOWNLOAD DB ----------------
@app.route("/download_db")
def download_db():
    if not session.get("admin"):
        return "Unauthorized", 403
    return send_file(DB_PATH, as_attachment=True)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

# ---------------- HOME ----------------
@app.route("/")
def home():
    if session.get("admin"):
        return redirect(url_for("admin_dashboard"))

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html", user=session["user"])

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        data = request.form

        bhk = int(data["bhk"])
        size = float(data["size"])
        floor = int(data["floor"])
        city = city_map[data["city"]]
        furnishing = furnishing_map[data["furnishing"]]
        bathroom = int(data["bathroom"])

        input_data = np.array([[bhk, size, floor, city, furnishing, bathroom]])
        prediction = np.expm1(model.predict(input_data))[0]

        return render_template("index.html",
                               prediction=round(prediction),
                               form_data=data)

    except Exception as e:
        print("Prediction Error:", e)
        return render_template("index.html", prediction="Error")

# ---------------- CONTACT ----------------
@app.route("/contact", methods=["POST"])
def contact():
    if "user" not in session:
        return jsonify({"status": "fail"})

    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # table create (ek baar chalega)
        c.execute("""
        CREATE TABLE IF NOT EXISTS contact(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
        """)

        c.execute("INSERT INTO contact (name,email,message) VALUES (?,?,?)",
                  (name, email, message))

        conn.commit()
        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        print("CONTACT ERROR:", e)
        return jsonify({"status": "fail"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
