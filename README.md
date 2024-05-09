# License Usage Dashboard

## Overview

This Flask application provides a dashboard for managing and viewing software license usage. It includes features to display data about license utilization per feature and daemon, enabling users to see total licenses, licenses in use, and licenses utilized by individual users.

## Features

- **Web Interface:** A user-friendly web interface to view and filter license usage data dynamically.
- **Database Interaction:** Utilizes SQLAlchemy for ORM-based interactions with a MySQL database, ensuring efficient data handling.
- **Data Visualization:** Displays data in a tabular format that can be filtered based on user inputs.
- **Dynamic Data Loading:** Supports loading data dynamically based on user interactions without the need to reload the page.

## Installation

Follow these steps to set up and run the application locally:

### Prerequisites

- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Pandas
- MySQL Database

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ia-usgs/ramvt3test.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database connection:**
   - Modify the `SQLALCHEMY_DATABASE_URI` in your application to point to your MySQL instance.

4. **Initialize the database:**
   - Ensure your MySQL server is running and the database schema is set up.

5. **Run the application:**
   ```bash
   python app.py
   ```

## Usage

Once the application is running, navigate to `http://localhost:8080` to access the dashboard. You can interact with the data through the provided web interface.

## API Endpoints

- **GET `/table_data/ramt_license_usage`**: Fetches all license usage data.
- **POST `/`**: Allows uploading and processing CSV data files to view data in the dashboard.

## Contributing

Contributions are welcome! Feel free to open pull requests with new features, fixes, or improvements.

## License

Distributed under the MIT License. See `LICENSE` for more information.