from flask import Flask, redirect, url_for, session, request, render_template
import os
import requests
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'  # Replace with a secure random key

# Set up the Google Fit API configuration
# Disable HTTPS requirement for local testing
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Update with your redirect URI if needed
REDIRECT_URI = 'http://localhost:8000/callback'
SCOPES = [
    # Basic user information scopes
    'openid',
    # See your primary Google Account email address
    'https://www.googleapis.com/auth/userinfo.email',
    # See your personal info, including any publicly available personal info
    'https://www.googleapis.com/auth/userinfo.profile',


    # Fitness API scopes for write access
    # Add to your Google Fit physical activity data
    'https://www.googleapis.com/auth/fitness.activity.write',
    # Add info about your blood glucose to Google Fit
    'https://www.googleapis.com/auth/fitness.blood_glucose.write',
    # Add info about your blood pressure in Google Fit
    'https://www.googleapis.com/auth/fitness.blood_pressure.write',
    # Add info about your body measurements to Google Fit
    'https://www.googleapis.com/auth/fitness.body.write',
    # Add to your heart rate data in Google Fit
    'https://www.googleapis.com/auth/fitness.heart_rate.write',
    # Add to info about your body temperature in Google Fit
    'https://www.googleapis.com/auth/fitness.body_temperature.write',
    # Add to your Google Fit location data
    'https://www.googleapis.com/auth/fitness.location.write',
    # Add to info about your nutrition in Google Fit
    'https://www.googleapis.com/auth/fitness.nutrition.write',
    # Add info about your oxygen saturation in Google Fit
    'https://www.googleapis.com/auth/fitness.oxygen_saturation.write',
    # Add info about your reproductive health in Google Fit
    'https://www.googleapis.com/auth/fitness.reproductive_health.write',
    # Add to your sleep data in Google Fit
    'https://www.googleapis.com/auth/fitness.sleep.write',


    # Fitness API scopes for read access
    # See and store your physical activity data
    'https://www.googleapis.com/auth/fitness.activity.read',
    # See info about your blood glucose in Google Fit
    'https://www.googleapis.com/auth/fitness.blood_glucose.read',
    # See info about your blood pressure in Google Fit
    'https://www.googleapis.com/auth/fitness.blood_pressure.read',
    # See info about your body measurements in Google Fit
    'https://www.googleapis.com/auth/fitness.body.read',
    # See your heart rate data in Google Fit
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    # See info about your body temperature in Google Fit
    'https://www.googleapis.com/auth/fitness.body_temperature.read',
    # See your Google Fit speed and distance data
    'https://www.googleapis.com/auth/fitness.location.read',
    # See info about your nutrition in Google Fit
    'https://www.googleapis.com/auth/fitness.nutrition.read',
    # See info about your oxygen saturation in Google Fit
    'https://www.googleapis.com/auth/fitness.oxygen_saturation.read',
    # See info about your reproductive health in Google Fit
    'https://www.googleapis.com/auth/fitness.reproductive_health.read',
    # See your sleep data in Google Fit
    'https://www.googleapis.com/auth/fitness.sleep.read'
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',  # Ensure this file contains your client ID and secret
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(access_type='offline')
    session['state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    if 'state' not in session:
        return "Error: State not found in session. Please try the authorization process again.", 400

    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES,
        state=session['state'],
        redirect_uri=REDIRECT_URI
    )
    try:
        flow.fetch_token(authorization_response=request.url)
    except Exception as e:
        return f"Error during token fetch: {str(e)}", 500

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('get_user_fit_data'))


@app.route('/fit_data')
def get_user_fit_data():
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources', headers=headers)

    if response.status_code == 200:
        if response.status_code == 200:
            fit_data = response.json()
            return render_template('fit_data copy.html', fit_data=fit_data)

    else:
        return f"Error fetching data: {response.text}"


@app.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


if __name__ == '__main__':
    # set port to 6000
    app.run(port=8000, debug=True)
