import sqlite3

conn = sqlite3.connect('loan_prediction.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(loan_predictions);")
columns = cursor.fetchall()
print(columns)
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

# Call this function to ensure the column exists
add_total_income_column()


conn = sqlite3.connect('loan_prediction.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(loan_predictions);")
columns = cursor.fetchall()
print(columns)
conn.close()
