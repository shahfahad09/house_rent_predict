# from flask import Flask, render_template, request, jsonify
# import numpy as np
# import joblib
# import smtplib

# app = Flask(__name__)

# # LOAD MODEL
# model = joblib.load("model/house_rent_rf_model.pkl")

# # CITY & FURNISHING MAP (same as training)
# city_map = {
#     "Bangalore": 0,
#     "Chennai": 1,
#     "Delhi": 2,
#     "Hyderabad": 3,
#     "Kolkata": 4,
#     "Mumbai": 5
# }

# furnishing_map = {
#     "Furnished": 0,
#     "Semi-Furnished": 1,
#     "Unfurnished": 2
# }

# # ---------------- HOME ----------------
# @app.route("/")
# def home():
#     return render_template("index.html")

# # ---------------- ABOUT ----------------
# @app.route("/about")
# def about():
#     return render_template("about.html")

# # ---------------- PREDICT ----------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         form_data = request.form

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

#     except Exception as e:
#         return render_template("index.html",
#                                prediction="Error",
#                                form_data=request.form)

# # ---------------- CONTACT (AJAX) ----------------
# @app.route("/contact", methods=["POST"])
# def contact():
#     try:
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']

#         # Your Gmail setup
#         sender_email = "khannishu522@gmail.com"      # sender gmail 
#         receiver_email = "khannishu522@gmail.com"    # receiver gmail
#         password = "zcqo lskh quij fmpi"             # Gmail App Password

#         full_message = f"Subject: New Contact Message\n\nName: {name}\nEmail: {email}\nMessage: {message}"

#         # SMTP mail send
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, full_message)
#         server.quit()

#         # AJAX response
#         return jsonify({"status": "success"})

#     except Exception as e:
#         print(e)
#         return jsonify({"status": "fail"})

# # ---------------- RUN ----------------
# # if __name__ == "__main__":
# #     app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import numpy as np
import joblib
import smtplib
import sqlite3
import bcrypt
import secrets

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 first_name TEXT,
                 last_name TEXT,
                 email TEXT UNIQUE,
                 phone TEXT UNIQUE,
                 password TEXT NOT NULL,
                 dob TEXT,
                 gender TEXT
                 )""")
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
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"].encode('utf-8')
        dob = request.form["dob"]
        gender = request.form["gender"]
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("""INSERT INTO users (first_name, last_name, email, phone, password, dob, gender)
                         VALUES (?,?,?,?,?,?,?)""",
                      (first_name, last_name, email, phone, hashed, dob, gender))
            conn.commit()
            conn.close()
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email or Phone already exists.", "danger")
            return render_template("signup.html")
    return render_template("signup.html")
# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT password,email FROM users WHERE email=? OR phone=?", (username, username))
        row = c.fetchone()
        conn.close()
        if row and bcrypt.checkpw(password,row[0]):
            session["user"] = row[1]  # store email in session
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials","danger")
            return render_template("login.html")
    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()  # saari login info remove kar do
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

@app.route("/about")
def about():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("about.html")

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))
    try:
        form_data = request.form
        bhk = int(form_data["bhk"])
        size = float(form_data["size"])
        floor = int(form_data["floor"])
        city = city_map[form_data["city"]]
        furnishing = furnishing_map[form_data["furnishing"]]
        bathroom = int(form_data["bathroom"])
        input_data = np.array([[bhk,size,floor,city,furnishing,bathroom]])
        prediction = np.expm1(model.predict(input_data))[0]
        return render_template("index.html", prediction=round(prediction), form_data=form_data)
    except:
        return render_template("index.html", prediction="Error", form_data=request.form)

# ---------------- CONTACT ----------------
@app.route("/contact", methods=["POST"])
def contact():
    if "user" not in session:
        return jsonify({"status":"fail","message":"Not logged in"})
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        sender_email = "khannishu522@gmail.com"
        receiver_email = "khannishu522@gmail.com"
        password = "zcqo lskh quij fmpi"
        full_message = f"Subject: New Contact Message\n\nName: {name}\nEmail: {email}\nMessage: {message}"
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,password)
        server.sendmail(sender_email,receiver_email,full_message)
        server.quit()
        return jsonify({"status":"success"})
    except Exception as e:
        print(e)
        return jsonify({"status":"fail"})

# ---------------- RUN ----------------
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)