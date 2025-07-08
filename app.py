import os
import sys
import logging
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import joblib
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global model variable
model = None

def load_model():
    """Load the trained Random Forest model with error handling"""
    global model
    try:
        if os.path.exists('random_forest_model.pkl'):
            model = joblib.load('random_forest_model.pkl')
            logger.info("Model loaded successfully")
            return True
        else:
            logger.error("Model file 'random_forest_model.pkl' not found")
            return False
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

# Database connection
def get_db_connection():
    """Get database connection with error handling"""
    try:
        conn = sqlite3.connect('loan_prediction.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def create_tables():
    """Create database tables"""
    try:
        conn = get_db_connection()
        if conn is None:
            return False
        
        # Create tables directly instead of using schema.sql
        cursor = conn.cursor()
        
        # Create loan_predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loan_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                married INTEGER,
                dependents INTEGER,
                education INTEGER,
                applicant_income REAL,
                coapplicant_income REAL,
                loan_amount REAL,
                loan_amount_term INTEGER,
                credit_history REAL,
                gender_male INTEGER,
                self_employed INTEGER,
                property_area_semiurban INTEGER,
                property_area_urban INTEGER,
                total_income REAL,
                prediction TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create contact_messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        return False

def add_total_income_column():
    """Add total_income column if it doesn't exist"""
    try:
        conn = get_db_connection()
        if conn is None:
            return False
            
        cursor = conn.cursor()
        
        # Check if the 'total_income' column exists
        cursor.execute("PRAGMA table_info(loan_predictions);")
        columns = cursor.fetchall()
        
        # If the column is missing, add it
        if not any(column[1] == 'total_income' for column in columns):
            cursor.execute("ALTER TABLE loan_predictions ADD COLUMN total_income REAL;")
            conn.commit()
            logger.info("Column 'total_income' added to the table.")
        else:
            logger.info("Column 'total_income' already exists.")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error adding total_income column: {e}")
        return False

# Route for home page
@app.route('/')
def home():
    try:
        return render_template('home_page.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return f"<h1>Welcome to Loan Prediction App</h1><p>Error: {str(e)}</p>", 500

# Route for about page
@app.route('/about')
def about():
    try:
        return render_template('about_page.html')
    except Exception as e:
        logger.error(f"Error rendering about page: {e}")
        return f"<h1>About</h1><p>Error: {str(e)}</p>", 500

# Route for prediction page
@app.route('/prediction')
def prediction():
    try:
        return render_template('predict.html')
    except Exception as e:
        logger.error(f"Error rendering prediction page: {e}")
        return f"<h1>Prediction</h1><p>Error: {str(e)}</p>", 500

# Route for contact page
@app.route('/contact')
def contact():
    try:
        return render_template('contact.html')
    except Exception as e:
        logger.error(f"Error rendering contact page: {e}")
        return f"<h1>Contact</h1><p>Error: {str(e)}</p>", 500

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'database_connected': get_db_connection() is not None
    })

# Route to handle prediction
@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return prediction()
    
    try:
        # Check if model is loaded
        if model is None:
            return render_template('predict.html', 
                                 prediction_text='Error: Model not loaded. Please try again later.')
        
        # Get input data from the form
        married = int(request.form.get('Married', 0))
        dependents = int(request.form.get('Dependents', 0))
        education = int(request.form.get('Education', 0))
        applicant_income = float(request.form.get('ApplicantIncome', 0))
        coapplicant_income = float(request.form.get('CoapplicantIncome', 0))
        loan_amount = float(request.form.get('LoanAmount', 0))
        loan_amount_term = int(request.form.get('Loan_Amount_Term', 0))
        credit_history = float(request.form.get('Credit_History', 0))
        gender_male = int(request.form.get('Gender_Male', 0))
        self_employed_yes = int(request.form.get('Self_Employed_Yes', 0))
        property_area_semiurban = int(request.form.get('Property_Area_Semiurban', 0))
        property_area_urban = int(request.form.get('Property_Area_Urban', 0))
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
        prediction_result = 'Approved' if prediction[0] == 1 else 'Rejected'

        # Save prediction data to the database
        try:
            conn = get_db_connection()
            if conn:
                conn.execute('''
                    INSERT INTO loan_predictions 
                    (married, dependents, education, applicant_income, coapplicant_income, loan_amount,
                    loan_amount_term, credit_history, gender_male, self_employed, property_area_semiurban, 
                    property_area_urban, total_income, prediction)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (married, dependents, education, applicant_income, coapplicant_income, loan_amount,
                    loan_amount_term, credit_history, gender_male, self_employed_yes, property_area_semiurban, 
                    property_area_urban, total_income, prediction_result))
                conn.commit()
                conn.close()
                logger.info(f"Prediction saved: {prediction_result}")
        except Exception as db_error:
            logger.error(f"Database error: {db_error}")
            # Continue even if database save fails

        # Render the result on the HTML page
        return render_template('predict.html', prediction_text=f'Loan Application is: {prediction_result}')
    
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        logger.error(traceback.format_exc())
        return render_template('predict.html', 
                             prediction_text=f'Error occurred during prediction: {str(e)}')

# Route for handling contact form data
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        # Get contact form data
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        message = request.form.get('message', '')
        
        # Validate inputs
        if not name or not email or not message:
            return render_template('contact.html', 
                                 error_message='All fields are required.')
        
        # Store in the database
        conn = get_db_connection()
        if conn:
            conn.execute('''
                INSERT INTO contact_messages (name, email, message) 
                VALUES (?, ?, ?)''', 
                (name, email, message))
            conn.commit()
            conn.close()
            logger.info(f"Contact message saved from {email}")
        
        # Redirect to contact page with success message
        return render_template('contact.html', message_sent=True)
    
    except Exception as e:
        logger.error(f"Error in contact form: {e}")
        return render_template('contact.html', 
                             error_message=f'Error occurred: {str(e)}')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

# Initialize the app
def initialize_app():
    """Initialize database and model"""
    logger.info("Initializing application...")
    
    # Create tables
    if not create_tables():
        logger.error("Failed to create database tables")
    
    # Add total_income column
    if not add_total_income_column():
        logger.error("Failed to add total_income column")
    
    # Load model
    if not load_model():
        logger.error("Failed to load model")

# Initialize when the app starts
initialize_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)