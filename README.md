# House Rent Predictor 🏠💰

A Machine Learning-based web application that predicts house rent prices based on features like locality, BHK, size, furnishing status, and preferred tenant type. Built using Python, Flask, and Scikit-Learn.

🔗 **Live Demo:** [House Rent Predictor](https://house-rent-predict.onrender.com/)

---

## 🌐 Deployment Details (Important Note ⚠️)

This project is deployed on **Render**. Please note the following regarding the live database:
* **Database Limitation:** The application uses **Render's Free Tier PostgreSQL** for user authentication (`users.db`). 
* **30-Day Expiry:** Render's free PostgreSQL databases expire and are automatically deleted **30 days after creation**. If the database expires, user login/signup features might require a database reset or redeployment.

---

## 🚀 Features

* **Accurate Predictions:** Utilizes a trained Machine Learning model to estimate house rent.
* **User Authentication:** Secure user login and signup system powered by PostgreSQL.
* **Responsive UI:** Clean, interactive, and user-friendly web interface built with HTML and CSS.
* **Environment Configuration:** Secure credential management using `.env` files.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3
* **Backend:** Python, Flask
* **Database:** PostgreSQL (Free Tier on Render)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Deployment:** Render (configured via `Procfile`)

---

## 📂 Project Structure

```text
├── model/                  # Saved machine learning model files
├── static/                 # CSS styles and frontend assets
│   └── style.css
├── templates/              # HTML templates for Flask UI
│   └── index.html
├── .env.example            # Template for environment variables
├── .gitignore              # Files to ignore in Git tracking
├── House_Rent_Dataset.csv # Dataset used for training the model
├── Procfile                # Deployment configuration for Render
├── app.py                  # Main Flask application logic
├── model_train.py          # Script to clean data and train the ML model
├── requirements.txt        # Python dependencies
└── users.db                # SQLite database for local testing
