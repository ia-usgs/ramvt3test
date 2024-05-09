RAMTv3 Dashboard
This is a user dashboard application that displays license usage data in an HTML table. It allows users to load CSV files containing license usage data, visualize the data, and access the data through an API.

Installation
To run the application locally, follow these steps:

Clone the repository: git clone https://github.com/ia-usgs/ramvt3test.git
Navigate to the project directory: cd user-dashboard
Create a virtual environment: python -m venv env
Activate the virtual environment:
On Windows: env\Scripts\activate
On macOS and Linux: source env/bin/activate
Install the required dependencies: pip install -r requirements.txt
Set up the database:
Create a database and update the database configuration in config.py.
Make sure the database is properly configured and accessible.
Run the application: python app.py
Open a web browser and navigate to http://localhost:8080 to access the application.

Usage
Load CSV files:
Navigate to the home page (http://localhost:8080).
Click on one of the "Load Data" buttons to load a CSV file containing license usage data.
The data will be displayed in an HTML table.
Visualize the data:
The loaded CSV file is displayed in an HTML table on the home page.
The table shows the license usage data for each row in the CSV file.
You can filter and sort the table using the provided options.
Access the API:
The application also provides an API endpoint for retrieving the license usage data.
To access the API, navigate to http://localhost:8080/table_data/ramt_license_usage.
The API returns the license usage data in JSON format.
You can use this endpoint to integrate the application with other systems or build custom visualizations.

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

Technologies Used
Flask: A Python web framework for building web applications.
SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library.
HTML: Hypertext Markup Language for structuring the content of the web page.
CSS: Cascading Style Sheets for styling the web page.
JavaScript: A programming language for adding interactivity to the web page.