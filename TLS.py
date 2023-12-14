# Raj Patel    
# Pacific id:- 989445044

from flask import Flask, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure Flask-Session to use filesystem-based session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)

# Configure Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/mini_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your model classes
class Individuals(db.Model):
    individual_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    birthplace = db.Column(db.String(50), nullable=False)
    genetic_information = db.Column(db.String(255), nullable=False)
    addresses = db.relationship('Addresses', backref='individual', lazy=True)
    financial_accounts = db.relationship('FinancialAccounts', backref='individual', lazy=True)

class Addresses(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    individual_id = db.Column(db.Integer, db.ForeignKey('individuals.individual_id'), nullable=False)

class FinancialAccounts(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), nullable=False)
    routing_number = db.Column(db.String(20), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    individual_id = db.Column(db.Integer, db.ForeignKey('individuals.individual_id'), nullable=False)

# Route for data entry form
@app.route('/', methods=['GET', 'POST'])
def data_entry():
    if request.method == 'POST':
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

        # Create a new individual
        new_individual = Individuals(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            birthplace=birthplace,
            genetic_information=genetic_information
        )

        # Add the individual to the database
        db.session.add(new_individual)
        db.session.commit()

        # Create a new address
        new_address = Addresses(
            street_address=street_address,
            city=city,
            state=state,
            zip_code=zip_code,
            individual_id=new_individual.individual_id
        )

        # Add the address to the database
        db.session.add(new_address)

        # Create a new financial account
        new_account = FinancialAccounts(
            account_number=account_number,
            routing_number=routing_number,
            account_type=account_type,
            individual_id=new_individual.individual_id
        )

        # Add the financial account to the database
        db.session.add(new_account)

        # Commit changes
        db.session.commit()

    return render_template('index.html')

# Other routes and functionalities can be added here

if __name__ == '__main__':
    app.run(debug=True)
