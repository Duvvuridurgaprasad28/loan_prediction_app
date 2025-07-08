
# Loan Prediction Web Application

This is a web application built using **Flask** that predicts whether a loan application will be **approved** or **rejected** based on user input. The model uses a **Random Forest** classifier to predict loan approval.

## Features
- User-friendly form for entering details about the loan applicant.
- Loan prediction model based on various input features.
- Contact page to submit messages and feedback.
- Display of the result (approved or rejected) based on user input.
- All data (including user contact messages and loan prediction results) are stored in a SQLite database.

## Technologies Used
- **Flask**: Python web framework.
- **scikit-learn**: Machine learning library for the loan prediction model.
- **SQLite**: Database for storing loan predictions and contact messages.
- **HTML/CSS**: For the front-end interface.
- **Bootstrap**: For responsive design.

## Project Structure
```
/loan_prediction
│
├── /static
│   ├── /images            # Images used in the app (e.g., loan approval/rejection images)
│   ├── style.css          # Custom CSS for the app
│
├── /templates
│   ├── home_page.html     # Home page template
│   ├── about_page.html    # About page template
│   ├── contact_page.html  # Contact page template
│   ├── predict.html       # Prediction form
│   ├── index.html         # Display prediction result
│
├── app.py                 # Main Flask application
├── schema.sql             # SQL schema for creating database tables
├── random_forest_model.pkl # Trained Random Forest model for loan prediction
└── README.md              # This file
```

## Requirements

To run this application, you need Python installed on your machine.

1. Install the required Python libraries by running:
   ```bash
   pip install -r requirements.txt
   ```
   **Note:** Make sure you have **`scikit-learn`**, **`Flask`**, **`pandas`**, and **`joblib`** installed.

2. The model file (`random_forest_model.pkl`) is pre-trained. If you want to train a new model, you'll need to adjust the training script or use a new model file.

## Setup Instructions

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/loan_prediction.git
cd loan_prediction
```

### 2. Set up a virtual environment (optional, but recommended):

```bash
python -m venv myenv
source myenv/bin/activate  # For Windows: myenv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Create the SQLite database:

Run the Flask app or manually execute the `create_tables()` function to create the necessary tables in the database.

### 5. Run the Flask application:

```bash
python app.py
```

The app will be accessible in your web browser at `http://127.0.0.1:5000/`.

### 6. Test the Application:

1. Go to the **Home Page** to enter details about a loan applicant.
2. Use the **Contact Page** to send messages or feedback.
3. View the prediction results displayed after submitting the loan prediction form.

## Database Structure

This project uses an SQLite database to store the following:

### 1. **loan_predictions** Table
Stores the data submitted for loan prediction, including the input features and the predicted loan status (approved/rejected).

Columns:
- `id`: Primary key (auto-increment)
- `married`: 0 or 1 (whether the applicant is married)
- `dependents`: Number of dependents
- `education`: 0 or 1 (whether the applicant is a graduate)
- `applicant_income`: Income of the applicant
- `coapplicant_income`: Income of the coapplicant
- `loan_amount`: Requested loan amount
- `loan_amount_term`: Loan term in months
- `credit_history`: 0.0 or 1.0 (credit history status)
- `gender_male`: 0 or 1 (gender)
- `self_employed`: 0 or 1 (whether the applicant is self-employed)
- `property_area_semiurban`: 0 or 1 (whether the property is in a semiurban area)
- `property_area_urban`: 0 or 1 (whether the property is in an urban area)
- `total_income`: Combined income of the applicant and coapplicant
- `prediction`: Result of the prediction ("Approved" or "Rejected")

### 2. **contact_messages** Table
Stores contact form submissions.

Columns:
- `id`: Primary key (auto-increment)
- `name`: Name of the user submitting the message
- `email`: Email of the user
- `message`: Message content
- `timestamp`: Date and time of submission

## Contributing

If you'd like to contribute to the project, please fork the repository, create a new branch, and submit a pull request. We welcome bug fixes, feature requests, and improvements.

## License

This project is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.
