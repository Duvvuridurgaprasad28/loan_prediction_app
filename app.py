from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained Random Forest model
model = joblib.load('random_forest_model.pkl')

# Database connection
def get_db_connection():
    conn = sqlite3.connect('loan_prediction.db')  # SQLite database file
    conn.row_factory = sqlite3.Row
    return conn

# Create tables when the app starts
def create_tables():
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())  # Execute the schema SQL file
    conn.commit()
    conn.close()

def add_total_income_column():
    conn = sqlite3.connect('loan_prediction.db')
    cursor = conn.cursor()

    # Check if the 'total_income' column exists
    cursor.execute("PRAGMA table_info(loan_predictions);")
    columns = cursor.fetchall()

    # If the column is missing, add it
    if not any(column[1] == 'total_income' for column in columns):
        cursor.execute("ALTER TABLE loan_predictions ADD COLUMN total_income FLOAT;")
        conn.commit()
        print("Column 'total_income' added to the table.")
    else:
        print("Column 'total_income' already exists.")

    conn.close()


# Route for home page
@app.route('/')
def home():
    return render_template('home_page.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about_page.html')

# Route for prediction page
@app.route('/prediction')
def prediction():
    return render_template('predict.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to handle prediction
@app.route("/predict", methods=['POST'])
def predict():
    # Get input data from the form
    married = int(request.form['Married'])
    dependents = int(request.form['Dependents'])
    education = int(request.form['Education'])
    applicant_income = float(request.form['ApplicantIncome'])
    coapplicant_income = float(request.form['CoapplicantIncome'])
    loan_amount = float(request.form['LoanAmount'])
    loan_amount_term = int(request.form['Loan_Amount_Term'])
    credit_history = float(request.form['Credit_History'])
    gender_male = int(request.form['Gender_Male'])
    self_employed_yes = int(request.form['Self_Employed_Yes'])
    property_area_semiurban = int(request.form['Property_Area_Semiurban'])
    property_area_urban = int(request.form['Property_Area_Urban'])
    total_income = applicant_income + coapplicant_income
    
    # Prepare the data for prediction
    data = pd.DataFrame({
        'Married': [married],
        'Dependents': [dependents],
        'Education': [education],
        'ApplicantIncome': [applicant_income],
        'CoapplicantIncome': [coapplicant_income],
        'LoanAmount': [loan_amount],
        'Loan_Amount_Term': [loan_amount_term],
        'Credit_History': [credit_history],
        'Gender_Male': [gender_male],
        'Self_Employed_Yes': [self_employed_yes],
        'Property_Area_Semiurban': [property_area_semiurban],
        'Property_Area_Urban': [property_area_urban],
        'Total_Income': [total_income]
    })

    # Make the prediction
    prediction = model.predict(data)
    prediction = 'Approved' if prediction[0] == 1 else 'Rejected'

    # Save prediction data to the database
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO loan_predictions 
        (married, dependents, education, applicant_income, coapplicant_income, loan_amount,
        loan_amount_term, credit_history, gender_male, self_employed, property_area_semiurban, 
        property_area_urban, total_income, prediction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (married, dependents, education, applicant_income, coapplicant_income, loan_amount,
        loan_amount_term, credit_history, gender_male, self_employed_yes, property_area_semiurban, 
        property_area_urban, total_income, prediction))
    conn.commit()
    conn.close()

    # Render the result on the HTML page
    return render_template('predict.html', prediction_text=f'Loan Application is: {prediction}')

# Route for handling contact form data
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Get contact form data
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Store in the database
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO contact_messages (name, email, message) 
        VALUES (?, ?, ?)''', 
        (name, email, message))
    conn.commit()
    conn.close()

    # Redirect to contact page with success message
    return render_template('contact.html', message_sent=True)

# Initialize the tables when the app starts
create_tables()
add_total_income_column()

if __name__ == '__main__':
    app.run(debug=True)
