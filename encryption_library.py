# Raj Patel    
# Pacific id:- 989445044

import mysql.connector
from flask import Flask, render_template, request
from cryptography.fernet import Fernet

# Database configuration
app = Flask(__name__)

config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "mini_project",
}

# Generate a new key
SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)

# Print the key to use in your application
print("SECRET_KEY:", SECRET_KEY)


# Route for data entry form
@app.route('/', methods=['GET', 'POST'])
def data_entry():
    if request.method == 'POST':
        print(request.form)
        # Connect to the database
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # Extract data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        birthplace = request.form['birthplace']
        genetic_information = request.form['genetic_information']
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        account_number = request.form['account_number']
        routing_number = request.form['routing_number']
        account_type = request.form['account_type']

        # Encrypt sensitive information 
        encrypted_genetic_info = cipher_suite.encrypt(genetic_information.encode('utf-8'))
        encrypted_account_number = cipher_suite.encrypt(account_number.encode('utf-8'))
        encrypted_street_address = cipher_suite.encrypt(street_address.encode('utf-8'))
        encrypted_routing_number = cipher_suite.encrypt(routing_number.encode('utf-8'))
        



        # Prepare and execute SQL queries
        sql = "INSERT INTO Individuals (first_name, last_name, date_of_birth, birthplace, genetic_information) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, date_of_birth, birthplace, encrypted_genetic_info))
        db.commit()
        individual_id = cursor.lastrowid

        sql = "INSERT INTO Addresses (street_address, city, state, zip_code, individual_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (encrypted_street_address, city, state, zip_code, individual_id))

        sql = "INSERT INTO Financial_Accounts (account_number, routing_number, account_type, individual_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (encrypted_account_number,encrypted_routing_number, account_type, individual_id))

        # Commit changes and close the connection
        db.commit()
        db.close()

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
