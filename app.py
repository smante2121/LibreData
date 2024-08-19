from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
from datetime import datetime, timedelta
from vital.client import Vital
from vital.environment import VitalEnvironment
import os
from dotenv import load_dotenv
import logging


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VITAL_ENVIRONMENT = os.getenv("VITAL_ENV")
VITAL_REGION = os.getenv("VITAL_REGION")
VITAL_API_KEY = os.getenv("VITAL_API_KEY")
BASE_URL = "https://api.sandbox.tryvital.io"
DEMO_USER_ID = os.getenv("DEMO_USER_ID")
LIBREVIEW_EMAIL = os.getenv("USERNAME")
LIBREVIEW_PASSWORD = os.getenv("PASSWORD")


app = Flask(__name__)


client = Vital(
    api_key=VITAL_API_KEY,
    environment=VitalEnvironment.SANDBOX,
)

def connect_freestyle_libre(): # Function to connect the user to the Freestyle Libre provider using a custom practice
    token_response = client.link.token(user_id=DEMO_USER_ID)
    link_token = token_response.link_token
    logger.info(f"Generated link token: {link_token}")

    try:
        link_response = client.link.connect_email_auth_provider(
            provider="freestyle_libre",
            email=LIBREVIEW_EMAIL,
            vital_link_token=link_token
        )
        logger.info(f"Connected to freestyle_libre: {link_response}")
    except Exception as e:
        logger.error(f"Error connecting to freestyle_libre: {e}")


def convert_to_mg_dl(value, unit): # function to convert glucose values to mg/dL if necessary
    if unit == 'mmol/L':
        return value * 18.0  # Convert mmol/L to mg/dL
    return value

def get_glucose_data(user_id, start_date, end_date): # utility function to get glucose data
    headers = {
        "Accept": "application/json",
        "x-vital-api-key": VITAL_API_KEY,
    }
    logger.info(f"Fetching glucose data for user_id: {user_id} from {start_date} to {end_date}")
    response = requests.get(
        f"{BASE_URL}/v2/timeseries/{user_id}/glucose?start_date={start_date}&end_date={end_date}",
        headers=headers
    )
    if response.status_code == 200:
        logger.info("Successfully fetched glucose data")
        glucose_data = response.json()

        for reading in glucose_data:  # Format the timestamps and convert values to mg/dL
            reading['value'] = convert_to_mg_dl(reading['value'], reading['unit'])

        return glucose_data
    else:
        logger.error(f"Failed to fetch glucose data: {response.json()}")
        return {"error": response.json()}

@app.route('/')
def index():
    connect_freestyle_libre()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    logger.info("Handling request to '/' endpoint")

    glucose_data = get_glucose_data(DEMO_USER_ID, start_date, end_date)

    if 'error' in glucose_data:
        return render_template('error.html', error=glucose_data['error'])

    return render_template('index.html', glucose_data=glucose_data)

@app.route('/link')
def link():
    token_response = client.link.token(user_id=DEMO_USER_ID)
    link_token = token_response.link_token
    link_url = f"https://link.tryvital.io/?token={link_token}&env={VITAL_ENVIRONMENT}&region={VITAL_REGION}"
    return render_template('link.html', link_url=link_url)

@app.route('/redirect')
def redirect_url():
    state = request.args.get('state', 'unknown')
    return f"Link flow completed with state: {state}"

if __name__ == '__main__':
    app.run(debug=True)