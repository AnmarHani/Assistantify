from fastapi import FastAPI, Depends, HTTPException, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import requests
import time

app = FastAPI()

# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.secret_key = 'Password123'

# Set up the Google Fit API configuration
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
REDIRECT_URI = 'http://localhost:8000/callback'
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/fitness.activity.write',
    'https://www.googleapis.com/auth/fitness.blood_glucose.write',
    'https://www.googleapis.com/auth/fitness.blood_pressure.write',
    'https://www.googleapis.com/auth/fitness.body.write',
    'https://www.googleapis.com/auth/fitness.heart_rate.write',
    'https://www.googleapis.com/auth/fitness.body_temperature.write',
    'https://www.googleapis.com/auth/fitness.location.write',
    'https://www.googleapis.com/auth/fitness.nutrition.write',
    'https://www.googleapis.com/auth/fitness.oxygen_saturation.write',
    'https://www.googleapis.com/auth/fitness.reproductive_health.write',
    'https://www.googleapis.com/auth/fitness.sleep.write',
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.blood_glucose.read',
    'https://www.googleapis.com/auth/fitness.blood_pressure.read',
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.body_temperature.read',
    'https://www.googleapis.com/auth/fitness.location.read',
    'https://www.googleapis.com/auth/fitness.nutrition.read',
    'https://www.googleapis.com/auth/fitness.oxygen_saturation.read',
    'https://www.googleapis.com/auth/fitness.reproductive_health.read',
    'https://www.googleapis.com/auth/fitness.sleep.read'
]

# In-memory session for demonstration; use a proper session management system in production
session = {}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the index page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/authorize")
async def authorize():
    """Redirect to Google OAuth2 authorization page."""
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(access_type='offline')
    session['state'] = state
    return RedirectResponse(authorization_url)


@app.get("/logout", name="logout")
async def logout(request: Request):
    # Handle logout logic here (e.g., clear session or token)
    return {"message": "Logged out successfully"}


@app.get("/callback")
async def callback(request: Request):
    """Handle the callback from Google OAuth2."""
    if 'state' not in session:
        raise HTTPException(
            status_code=400, detail="State not found in session. Please try the authorization process again."
        )

    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES,
        state=session['state'],
        redirect_uri=REDIRECT_URI
    )
    try:
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during token fetch: {str(e)}"
        )

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return RedirectResponse(url='/fit_data')


@app.get("/fit_data", response_class=HTMLResponse)
async def get_user_fit_data(request: Request):
    """Fetch and display user fitness data."""
    if 'credentials' not in session:
        return RedirectResponse(url='/authorize')

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}

    now = int(time.time() * 1e9)
    all_the_time = 0  # Get all data

    # data sources used to fetch the data from Google Fit API
    data_sources = {
        'weight': 'derived:com.google.weight:com.google.android.gms:merge_weight',
        'height': 'derived:com.google.height:com.google.android.gms:merge_height',
        'active_minutes': 'derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes',
        'activity_segment': 'derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments',
        'bmr_calories': 'derived:com.google.calories.bmr:com.google.android.gms:merged',
        'expended_calories': 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended',
        'step_count': 'derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas',
        'distance': 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',
        'heart_minutes': 'raw:com.google.heart_minutes:com.google.android.apps.fitness:user_input',
        'speed': 'derived:com.google.speed:com.google.android.gms:merge_speed',
        'heart_rate': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm',
        'oxygen_saturation': 'derived:com.google.oxygen_saturation:com.google.android.gms:merge_oxygen_saturation',
        'body_temperature': 'derived:com.google.body.temperature:com.google.android.gms:merge_body_temperature',
        'blood_pressure': 'derived:com.google.blood_pressure:com.google.android.gms:merge_blood_pressure',
        'blood_glucose': 'derived:com.google.blood_glucose:com.google.android.gms:merge_blood_glucose',
        'sleep': 'derived:com.google.sleep.segment:com.google.android.gms:merge_sleep_segments',
        'location': 'derived:com.google.location.sample:com.google.android.gms:merge_location_samples',
        'nutrition': 'derived:com.google.nutrition:com.google.android.gms:merge_nutrition',
        'reproductive_health': 'derived:com.google.reproductive_health:com.google.android.gms:merge_reproductive_health',
        'body': 'derived:com.google.body.fat_percentage:com.google.android.gms:merge_body_fat_percentage',
        'workout': 'derived:com.google.workout.exercise:com.google.android.gms:merge_workout_exercise',
    }

    # Fetch each dataset
    responses = {}
    for key, data_source in data_sources.items():
        response = requests.get(
            f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{data_source}/datasets/{int(all_the_time)}-{int(now)}',
            headers=headers
        )
        responses[key] = response

    # Check for success and extract data
    if all(response.status_code == 200 for response in responses.values()):
        weight_data = responses['weight'].json().get('point', [])
        height_data = responses['height'].json().get('point', [])

        active_minutes_data = responses['active_minutes'].json()
        activity_segment_data = responses['activity_segment'].json()
        bmr_calories_data = responses['bmr_calories'].json()
        expended_calories_data = responses['expended_calories'].json()
        step_count_data = responses['step_count'].json()
        distance_data = responses['distance'].json()
        heart_minutes_data = responses['heart_minutes'].json()
        speed_data = responses['speed'].json()
        heart_rate_data = responses['heart_rate'].json()
        oxygen_saturation_data = responses['oxygen_saturation'].json()
        body_temperature_data = responses['body_temperature'].json()
        blood_pressure_data = responses['blood_pressure'].json()
        blood_glucose_data = responses['blood_glucose'].json()
        sleep_data = responses['sleep'].json()
        location_data = responses['location'].json()
        nutrition_data = responses['nutrition'].json()
        reproductive_health_data = responses['reproductive_health'].json()
        body_data = responses['body'].json()
        workout_data = responses['workout'].json()

        fit_data = {
            "request": request,
            "Weight": weight_data,
            "Height": height_data,
            "Active Minutes": active_minutes_data,
            "Activity Segment": activity_segment_data,
            "BMR Calories": bmr_calories_data,
            "Expended Calories": expended_calories_data,
            "Step Count": step_count_data,
            "Distance": distance_data,
            "Heart Minutes": heart_minutes_data,
            "Speed": speed_data,
            "Heart Rate": heart_rate_data,
            "Oxygen Saturation": oxygen_saturation_data,
            "Body Temperature": body_temperature_data,
            "Blood Pressure": blood_pressure_data,
            "Blood Glucose": blood_glucose_data,
            "Sleep": sleep_data,
            "Location": location_data,
            "Nutrition": nutrition_data,
            "Reproductive Health": reproductive_health_data,
            "Body": body_data,
            "Workout": workout_data
        }

        return templates.TemplateResponse('fit_data.html', {
            "request": request,
            "fit_data": fit_data  # Pass the dictionary to the template
        })


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }


def extract_weight_and_height(weight_data, height_data):
    """Extract weight and height from Google Fit data."""
    weight_data = weight_data[-1].get('value', [{}])
    height_data = height_data[-1].get('value', [{}])

    weight_value = weight_data[-1].get('fpVal', 0) if weight_data else 0
    height_value = height_data[-1].get('fpVal', 0) if height_data else 0

    return weight_value, height_value


def extract_active_minutes(response):
    # Check if response is a list and has points
    if isinstance(response, list) and response:
        return response[-1].get('value', {}).get('intVal', 0)
    return 0


def extract_activity_segment(response):
    # Check if response is a list and has points
    if isinstance(response, list) and response:
        # Access the last point in the list
        last_segment = response[-1].get('point', [{}])
        if last_segment:
            return last_segment[-1].get('value', {}).get('intVal', 0)
    return 0


def extract_bmr_calories(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('intVal', 0)
    return 0


def extract_step_count(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('intVal', 0)
    return 0


def extract_distance(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_heart_minutes(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('intVal', 0)
    return 0


def extract_speed(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_heart_rate(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_oxygen_saturation(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_body_temperature(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_blood_pressure(response):
    if isinstance(response, list) and response:
        return response[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_blood_glucose(response):
    if isinstance(response, list) and response:
        return response[-1].get('value', {}).get('fpVal', 0)
    return 0


def extract_sleep(response):
    print(response)
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('intVal', 0)
    return 0


def extract_nutrition(response):
    if isinstance(response, list) and response:
        return response[-1].get('point', [{}])[-1].get('value', {}).get('intVal', 0)
    return 0


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
