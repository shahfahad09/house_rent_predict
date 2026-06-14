# House Rent Predictor 🏠💰

A Machine Learning-based web application that predicts house rent prices based on features like locality, BHK, size, furnishing status, and preferred tenant type. Built using Python, Flask, and Scikit-Learn, and deployed on Render.

🔗 **Live Demo:** [House Rent Predictor](https://house-rent-predict.onrender.com/)

---

## 🚀 Features

* **Accurate Predictions:** Utilizes a trained Machine Learning model to estimate house rent.
* **User Authentication:** Secure user login and signup system powered by SQLite (`users.db`).
* **Responsive UI:** Clean, interactive, and user-friendly web interface built with HTML and CSS.
* **Environment Configuration:** Secure credential management using `.env` files.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3
* **Backend:** Python, Flask
* **Database:** SQLite (`users.db` for user authentication)
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
└── users.db                # SQLite database for storing user accounts



🔧 Installation & Local Setup
To run this project locally on your machine, follow these steps:

1. Clone the Repository
Bash
git clone [https://github.com/shahfahad09/house_rent_predict.git](https://github.com/shahfahad09/house_rent_predict.git)
cd house_rent_predict
2. Create a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Setup Environment Variables
Copy the .env.example file to a new file named .env and configure your secret keys if required.

Bash
cp .env.example .env
5. Train the Model (Optional)
If you want to re-train or generate the model file from the dataset:

Bash
python model_train.py
6. Run the Flask Server
Bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000/.

🌐 Deployment
This project is configured for easy deployment on platforms like Render or Heroku using the provided Procfile.

The live version is currently hosted at:
👉 https://house-rent-predict.onrender.com/

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

Fork the project.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

👤 Author
MD SHAHFAHAD KHAN - @shahfahad09
