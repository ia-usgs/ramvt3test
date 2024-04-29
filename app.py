import os

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


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
    

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8080))
    app.run(port=port, host='0.0.0.0', debug=True)