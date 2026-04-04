# app.py (Multi-user safe, PostgreSQL version)
from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
import numpy as np
import joblib
import smtplib
import bcrypt
import psycopg2
from psycopg2 import pool

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# ---------------- ADMIN ----------------
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# ---------------- DATABASE POOL ----------------
DB_POOL = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min 1, max 20 connections
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", "5432"),
    database=os.environ.get("DB_NAME", "house_rent_db")
)

def get_db():
    return DB_POOL.getconn()

def release_db(conn):
    DB_POOL.putconn(conn)

# ---------------- INIT DB ----------------
def init_db():
    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                phone TEXT UNIQUE,
                password BYTEA,
                dob TEXT,
                gender TEXT
            )
            """)
        conn.commit()
    finally:
        release_db(conn)

init_db()

# ---------------- ML MODEL ----------------
model = joblib.load("model/house_rent_rf_model.pkl")
city_map = {"Bangalore":0,"Chennai":1,"Delhi":2,"Hyderabad":3,"Kolkata":4,"Mumbai":5}
furnishing_map = {"Furnished":0,"Semi-Furnished":1,"Unfurnished":2}

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"].encode('utf-8')
        dob = request.form["dob"]
        gender = request.form["gender"]

        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_db()
        try:
            with conn.cursor() as c:
                c.execute("""
                INSERT INTO users (first_name, last_name, email, phone, password, dob, gender)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (first_name, last_name, email, phone, hashed, dob, gender))
            conn.commit()
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("Email or Phone already exists.", "danger")

        except Exception as e:
            conn.rollback()
            print("Signup Error:", e)
            flash("Something went wrong!", "danger")

        finally:
            release_db(conn)

    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password").encode('utf-8')

        conn = get_db()
        try:
            with conn.cursor() as c:
                c.execute("SELECT password,email FROM users WHERE email=%s OR phone=%s", (username, username))
                row = c.fetchone()
        finally:
            release_db(conn)

        if row:
          
            stored_password = bytes(row[0]) 
            
            if bcrypt.checkpw(password, stored_password):
                session.clear()
                session["user"] = row[1]
                return redirect(url_for("home"))

        flash("Invalid credentials", "danger")
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
import csv
from io import StringIO
from flask import Response

@app.route("/download_db")
def download_db():
    if not session.get("admin"):
        return "Unauthorized", 403

    conn = get_db()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM users")
            rows = c.fetchall()
            colnames = [desc[0] for desc in c.description]

        # CSV generate
        si = StringIO()
        writer = csv.writer(si)
        writer.writerow(colnames)  # header
        writer.writerows(rows)

        output = si.getvalue()
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition":"attachment;filename=users.csv"}
        )
    finally:
        release_db(conn)

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

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
