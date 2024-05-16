import os

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:kali@172.30.158.175:3306/ramtdb'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route for the main page of the application.
    It handles both GET and POST requests.
    Keep in mind that this route is only to be used if only loading from a csv file, in this case
    it is not needed since we are loading from a database. If no database is around, then use the code here to load it
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

    # It is a string column with a maximum length of 50 characters.
    feature_name = db.Column(db.String(50))


    # It is a string column with a maximum length of 50 characters.
    licenses_total = db.Column(db.String(50))


    # It is a string column with a maximum length of 50 characters.
    licenses_total_in_use = db.Column(db.String(50))


    # It is a string column with a maximum length of 50 characters.
    licenses_total = db.Column(db.String(50))

    licenses_used_by_user = db.Column(db.Integer)

    expiration_date = db.Column(db.String)


@app.route('/table_data/ramt_license_usage', methods=['GET'])
def table_data():
    users = User.query.all()
    data = [
        {
            # Map each User object to a dictionary containing its attributes.
            #
            # :return: A list of dictionaries representing the User objects.
            # Each dictionary contains the attributes 'license_usage_id',
            # 'daemon_name', 'feature_name', 'licenses_total',
            # 'licenses_total_in_use', and 'licenses_used_by_user'.
            # The values of these attributes are the corresponding attributes of the User object.
            "license_usage_id": user.license_usage_id,
            # The daemon name of the user.
            "daemon_name": user.daemon_name,
            # The feature name of the user.
            "feature_name": user.feature_name,
            # The total number of licenses of the user.
            "licenses_total": user.licenses_total,
            # The number of licenses used by the user.
            "licenses_total_in_use": user.licenses_total_in_use,
            # The number of licenses used by the user.
            "licenses_used_by_user": user.licenses_used_by_user,

            "expiration_date": user.expiration_date,

        }
        for user in users
    ]
    return jsonify(data)


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8080))
    app.run(port=port, host='0.0.0.0', debug=True)


