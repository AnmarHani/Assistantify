from flask import Flask, redirect, url_for, session, request, render_template
import os
import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import time  # To get the current timestamp in nanoseconds

app = Flask(__name__)
app.secret_key = 'Password123'

# Set up the Google Fit API configuration
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.location.read'
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
    authorization_url, state = flow.authorization_url(
        access_type='offline')  # Offline for refresh token
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
    print(session)
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}

    # Calculate the start and end times in nanoseconds (Unix timestamp * 1e9)
    now = int(time.time() * 1e9)
    # A week ago in nanoseconds put zero if you want to get all data
    one_week_ago = now - (7 * 24 * 60 * 60 * 1e9)

    # Fetch weight data with correct datasetId (startTime-endTime in nanoseconds)
    weight_data = requests.get(
        f'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/datasets/{int(one_week_ago)}-{int(now)}',
        headers=headers)

    # Fetch height data with correct datasetId
    height_data = requests.get(
        f'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.height:com.google.android.gms:merge_height/datasets/{int(one_week_ago)}-{int(now)}',
        headers=headers)

    if weight_data.status_code == 200 and height_data.status_code == 200:
        weight_value, height_value = extract_weight_and_height(
            weight_data.json(), height_data.json())
        return render_template('fit_data.html', weight=weight_value, height=height_value)
    else:
        return f"Error fetching data: {weight_data.text if weight_data.status_code != 200 else height_data.text}"


@app.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))


def extract_weight_and_height(weight_data, height_data):
    weight = "Unavailable"
    height = "Unavailable"

    # Extract weight
    if 'point' in weight_data and weight_data['point']:
        # Assuming we're only interested in the first point
        weight_point = weight_data['point'][-1]
        if 'value' in weight_point and weight_point['value']:
            weight = weight_point['value'][0].get('fpVal', "Unavailable")

    # Extract height
    if 'point' in height_data and height_data['point']:
        # Assuming we're only interested in the first point
        height_point = height_data['point'][-1]
        if 'value' in height_point and height_point['value']:
            height = height_point['value'][0].get('fpVal', "Unavailable")

    return weight, height


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
    app.run(debug=True)
