import json
import os

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Load CSV file, skip the first 5 rows, and assume the first row of data has the headers.
        data = pd.read_csv('TEST 2024-V2 RAMTV3.csv', skiprows=6) # you need to update the path here in order to read the file as well as the name
        # Convert DataFrame to HTML
        data_html = data.to_html(classes='table table-striped')
        return render_template('index.html', data_html=data_html)
    return render_template('index.html', data_html=None)



if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 8080))
    app.run(port=port, host='0.0.0.0', debug=True)
