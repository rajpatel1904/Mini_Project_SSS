# Raj Patel    
# Pacific id:- 989445044

import mysql.connector
from flask import Flask, render_template, request, send_from_directory

# Database configuration
app = Flask(__name__)
# Replace with your actual connection details
config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "mini_project",
}

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

        # Prepare and execute SQL queries
        sql = "INSERT INTO Individuals (first_name, last_name, date_of_birth, birthplace, genetic_information) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, date_of_birth, birthplace, genetic_information))
        db.commit()
        individual_id = cursor.lastrowid

        sql = "INSERT INTO Addresses (street_address, city, state, zip_code,individual_id) VALUES (%s, %s, %s, %s,%s)"
        cursor.execute(sql, (street_address, city, state, zip_code,individual_id))

        sql = "INSERT INTO Financial_Accounts (account_number, routing_number, account_type, individual_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (account_number, routing_number, account_type, individual_id))


        # Commit changes and close the connection
        db.commit()
        db.close()

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
