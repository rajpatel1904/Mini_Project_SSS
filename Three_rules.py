import os
import datetime
import mysql.connector
from flask import Flask, render_template, request
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Database configuration
app = Flask(__name__)

# Use environment variables for database credentials
# RULE:-3  SECRETS MANAGMENT
config = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "root"),
    "database": os.environ.get("DB_DATABASE", "mini_project"),
}

secret_key = os.urandom(32)
cipher_suite = AESGCM(secret_key)

# Function for encrypting sensitive data using AES-GCM
def encrypt_data(data):
    if isinstance(data, str):
        # For simplicity, using an empty string as associated_data
        associated_data = b""
        ciphertext = cipher_suite.encrypt(associated_data, data.encode('utf-8'))
        return ciphertext.hex()
    else:
        return data


@app.route('/', methods=['GET', 'POST'])
def data_entry():
    if request.method == 'POST':                                                   
        try:
            # RULE 2:- INPUT VALIDATION ERROR
            if (
                len(request.form['first_name']) >= 50
                or len(request.form['last_name']) >= 50
                or not (8 <= len(request.form['account_number']) <= 9)
                or not (len(request.form['routing_number']) == 9)
            ):
                raise ValueError("Invalid input. Please check your data.")

            datetime.datetime.strptime(request.form['date_of_birth'], "%Y-%m-%d")
        except ValueError as error:
            # Log the error for debugging purposes
            app.logger.error(f"Validation error: {error}")
            return render_template('validation_error.html')

        # Extract and encrypt sensitive data
        encrypted_genetic_info = encrypt_data(request.form['genetic_information'])
        encrypted_account_number = encrypt_data(request.form['account_number'])
        encrypted_street_address = encrypt_data(request.form['street_address'])

        # Connect to the database
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # Prepare and execute SQL queries with placeholders
        sql_individual = "INSERT INTO Individuals (first_name, last_name, date_of_birth, birthplace, genetic_information) VALUES (%s, %s, %s, %s, %s)"
        sql_address = "INSERT INTO Addresses (street_address, city, state, zip_code, individual_id) VALUES (%s, %s, %s, %s, %s)"
        sql_financial_account = "INSERT INTO Financial_Accounts (account_number, routing_number, account_type, individual_id) VALUES (%s, %s, %s, %s)"


        # RULE:-1  SQL INJECTION
        cursor.execute(sql_individual, (request.form['first_name'], request.form['last_name'], request.form['date_of_birth'], request.form['birthplace'], encrypted_genetic_info))
        cursor.execute(sql_address, (encrypted_street_address, request.form['city'], request.form['state'], request.form['zip_code'], cursor.lastrowid))
        cursor.execute(sql_financial_account, (encrypted_account_number, request.form['routing_number'], request.form['account_type'], cursor.lastrowid))

        # Commit changes and close the connection
        db.commit()
        db.close()

        return render_template('index.html')  # Adjust the template name as needed

    # Return a response for other request methods (e.g., 'GET')
    return render_template('index.html')  # Adjust the template name as needed

if __name__ == '__main__':
    # Enable debug mode only during development
    app.run(debug=True)
