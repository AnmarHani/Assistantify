from flask import Flask, redirect, url_for, session, request, render_template
import os
import requests
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import time

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
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}

    # Calculate the start and end times in nanoseconds (Unix timestamp * 1e9)
    now = int(time.time() * 1e9)
    all_the_time = 0  # Get all data

    # Fetch data from various Google Fit streams
    data_sources = {
        'weight': 'derived:com.google.weight:com.google.android.gms:merge_weight',
        'height': 'derived:com.google.height:com.google.android.gms:merge_height',
        'active_minutes': 'derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes',
        'activity_segment': 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments',
        'bmr_calories': 'derived:com.google.calories.bmr:com.google.android.gms:merged',
        'expended_calories': 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended',
        'step_count': 'derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas',
        'distance': 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',
        'heart_minutes': 'derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes',
        'speed': 'derived:com.google.speed:com.google.android.gms:merge_speed'
    }

    # Fetch each dataset
    responses = {}
    for key, data_source in data_sources.items():
        responses[key] = requests.get(
            f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{data_source}/datasets/{int(all_the_time)}-{int(now)}',
            headers=headers
        )

    # Check for success and extract data
    if all(response.status_code == 200 for response in responses.values()):
        weight_value, height_value = extract_weight_and_height(
            responses['weight'].json(), responses['height'].json())
        active_minutes_value = extract_active_minutes(
            responses['active_minutes'].json())
        activity_segment_value = extract_activity_segment(
            responses['activity_segment'].json())
        bmr_calories_value = extract_bmr_calories(
            responses['bmr_calories'].json())
        expended_calories_value = extract_bmr_calories(
            responses['expended_calories'].json())  # Same logic for calories
        step_count_value = extract_step_count(responses['step_count'].json())
        distance_value = extract_distance(responses['distance'].json())
        heart_minutes_value = extract_heart_minutes(
            responses['heart_minutes'].json())
        speed_value = extract_speed(responses['speed'].json())

        return render_template('fit_data.html', weight=weight_value, height=height_value,
                               active_minutes=active_minutes_value, activity_segment=activity_segment_value,
                               bmr_calories=bmr_calories_value, expended_calories=expended_calories_value,
                               step_count=step_count_value, distance=distance_value,
                               heart_minutes=heart_minutes_value, speed=speed_value)
    else:
        return "Error fetching data."


@app.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))


# Extraction functions for various data
def extract_weight_and_height(weight_data, height_data):
    weight = "Unavailable"
    height = "Unavailable"

    # Extract weight
    if 'point' in weight_data and weight_data['point']:
        weight_point = weight_data['point'][-1]
        if 'value' in weight_point and weight_point['value']:
            weight = weight_point['value'][0].get('fpVal', "Unavailable")

    # Extract height
    if 'point' in height_data and height_data['point']:
        height_point = height_data['point'][-1]
        if 'value' in height_point and height_point['value']:
            height = height_point['value'][0].get('fpVal', "Unavailable")

    return weight, height


def extract_active_minutes(active_minutes_data):
    active_minutes = "Unavailable"
    if 'point' in active_minutes_data and active_minutes_data['point']:
        active_minutes_point = active_minutes_data['point'][-1]
        if 'value' in active_minutes_point and active_minutes_point['value']:
            active_minutes = active_minutes_point['value'][0].get(
                'intVal', "Unavailable")
    return active_minutes


def extract_activity_segment(activity_segment_data):
    activity = "Unavailable"
    if 'point' in activity_segment_data and activity_segment_data['point']:
        activity_point = activity_segment_data['point'][-1]
        if 'value' in activity_point and activity_point['value']:
            activity = activity_point['value'][0].get('intVal', "Unavailable")
    return activity


def extract_bmr_calories(bmr_calories_data):
    calories = "Unavailable"
    if 'point' in bmr_calories_data and bmr_calories_data['point']:
        calories_point = bmr_calories_data['point'][-1]
        if 'value' in calories_point and calories_point['value']:
            calories = calories_point['value'][0].get('fpVal', "Unavailable")
    return calories


def extract_step_count(step_count_data):
    steps = "Unavailable"
    if 'point' in step_count_data and step_count_data['point']:
        step_point = step_count_data['point'][-1]
        if 'value' in step_point and step_point['value']:
            steps = step_point['value'][0].get('intVal', "Unavailable")
    return steps


def extract_distance(distance_data):
    distance = "Unavailable"
    if 'point' in distance_data and distance_data['point']:
        distance_point = distance_data['point'][-1]
        if 'value' in distance_point and distance_point['value']:
            distance = distance_point['value'][0].get('fpVal', "Unavailable")
    return distance


def extract_heart_minutes(heart_minutes_data):
    heart_minutes = "Unavailable"
    if 'point' in heart_minutes_data and heart_minutes_data['point']:
        heart_minutes_point = heart_minutes_data['point'][-1]
        if 'value' in heart_minutes_point and heart_minutes_point['value']:
            heart_minutes = heart_minutes_point['value'][0].get(
                'fpVal', "Unavailable")
    return heart_minutes


def extract_speed(speed_data):
    speed = "Unavailable"
    if 'point' in speed_data and speed_data['point']:
        speed_point = speed_data['point'][-1]
        if 'value' in speed_point and speed_point['value']:
            speed = speed_point['value'][0].get('fpVal', "Unavailable")
    return speed


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
