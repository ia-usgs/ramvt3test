import os

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kali@localhost/ramtdb'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route for the main page of the application.
    It handles both GET and POST requests.
    """
    if request.method == 'POST':
        # Get the name of the button clicked from the form data
        button_clicked = request.form.get('button')
        print(f"button_clicked: {button_clicked}")  # print the button name for debugging
        
        # Load the corresponding CSV file based on the button clicked
        if button_clicked == 'Load Data 1':
            # The name 'Load Data' is hard-coded in the HTML template
            df = pd.read_csv('TEST 2024-V2 RAMTV3.csv', skiprows=6)
        elif button_clicked == 'Load Data 2':
            df = pd.read_csv('4084_asdsls30.csv')
        elif button_clicked == 'Load Data 3':
            df = pd.read_csv('4084_sarebraslic81.csv')
        else:
            df = None
        
        # Generate HTML table from the DataFrame
        if df is not None:
            data_html = df.to_html(classes='table table-striped table-bordered')
        else:
            data_html = None
        
        # Render the index.html template with the generated HTML table
        return render_template('index.html', data_html=data_html)
    else:
        # If it's a GET request, render the index.html template without any data
        return render_template('index.html')



class User(db.Model):
    # The __tablename__ attribute sets the name of the database table
    # to 'users'.
    __tablename__ = 'ramt_license_usage'

    license_usage_id = db.Column(db.Integer, primary_key=True)


    # The 'id' column is the primary key of the 'users' table.
    # It is an integer column.
    daemon_name = db.Column(db.Integer)

    # The 'name' column stores the name of the user.
    # It is a string column with a maximum length of 50 characters.
    feature_name = db.Column(db.String(50))

    # The 'age' column stores the age of the user.
    # It is a string column with a maximum length of 50 characters.
    licenses_total = db.Column(db.String(50))

    # The 'address' column stores the address of the user.
    # It is a string column with a maximum length of 50 characters.
    licenses_total_in_use = db.Column(db.String(50))

    # The 'salary' column stores the salary of the user.
    # It is a string column with a maximum length of 50 characters.
    licenses_total = db.Column(db.String(50))

    licenses_used_by_user = db.Column(db.Integer)


@app.route('/table_data/ramt_license_usage')
def table_data():
    users = User.query.all()
    data = [
        {
            'license_usage_id': user.license_usage_id,
            'daemon_name': user.daemon_name,
            'feature_name': user.feature_name,
            'licenses_total': user.licenses_total,
            'licenses_total_in_use': user.licenses_total_in_use,
            'licenses_used_by_user': user.licenses_used_by_user,
        }
        for user in users
    ]
    return jsonify(data)


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8080))
    app.run(port=port, host='0.0.0.0', debug=True)


