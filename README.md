# LibreData

## Overview
**LibreData** is a Flask application designed to interface with the TryVital API to access glucose data for users of the Freestyle Libre glucose monitoring device. This project aims to retrieve glucose data from the TryVital API and eventually store it in a Google Cloud database for further analysis. The goal is to provide users with in-depth insights into their glucose levels, which will help them better manage their health.

## Features
- **TryVital API Integration**: Connects to the Freestyle Libre provider via TryVital API to fetch glucose data.
- **Glucose Data Conversion**: Converts glucose values to mg/dL if they are provided in mmol/L.
- **Data Retrieval**: Fetches glucose data for a user over a specified time range.
- **Flask Framework**: Utilizes Flask to handle HTTP requests and render templates for displaying glucose data.
- **Logging and Error Handling**: Implements logging to track the process and handle errors gracefully.

## How It Works
1. **Freestyle Libre Connection**: The application connects to the Freestyle Libre provider using TryVital's `link.connect_email_auth_provider()` method, which authenticates via the user's email.
2. **Glucose Data Fetching**: The application retrieves glucose data for a specified date range and converts the values to mg/dL if needed.
3. **Displaying Data**: The data is rendered on a webpage using Flask's `render_template()` method.

## Project Structure
- **main.py**: The main application file that handles API connections, data retrieval, and Flask routes.
- **templates/**: Contains HTML templates for rendering web pages.
- **.env**: Stores environment variables like API keys and user credentials (not included in the repository for security reasons).
- **requirements.txt**: Lists the Python dependencies needed to run the project.

## Future Work
- **Google Cloud Integration**: The glucose data will be extracted and stored in a Google Cloud database for further analysis.
- **Data Analysis**: Develop tools to analyze the stored glucose data and provide users with detailed insights into their glucose trends.
- **Expanded Functionality**: Add more features to help users manage their glucose levels, such as alerts for high or low glucose readings.
