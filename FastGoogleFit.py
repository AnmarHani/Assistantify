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
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.location.read'
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


@app.get("/callback")
async def callback(request: Request):
    """Handle the callback from Google OAuth2."""
    if 'state' not in session:
        raise HTTPException(
            status_code=400, detail="State not found in session. Please try the authorization process again.")

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
            status_code=500, detail=f"Error during token fetch: {str(e)}")

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
        response = requests.get(
            f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{data_source}/datasets/{int(all_the_time)}-{int(now)}',
            headers=headers
        )
        responses[key] = response

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

        return templates.TemplateResponse('fit_data.html', {
            "request": request,
            "weight": weight_value,
            "height": height_value,
            "active_minutes": active_minutes_value,
            "activity_segment": activity_segment_value,
            "bmr_calories": bmr_calories_value,
            "expended_calories": expended_calories_value,
            "step_count": step_count_value,
            "distance": distance_value,
            "heart_minutes": heart_minutes_value,
            "speed": speed_value
        })
    else:
        raise HTTPException(status_code=500, detail="Error fetching data.")


@app.get("/logout")
async def logout():
    """Log the user out and clear the session."""
    session.pop('credentials', None)
    return RedirectResponse(url='/')

# Endpoints for each extraction function


@app.get("/weight")
async def get_weight():
    """Get user's weight data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.weight:com.google.android.gms:merge_weight/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return extract_weight_and_height(response.json(), {})


@app.get("/height")
async def get_height():
    """Get user's height data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.height:com.google.android.gms:merge_height/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return extract_weight_and_height({}, response.json())


@app.get("/active_minutes")
async def get_active_minutes():
    """Get user's active minutes data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"active_minutes": extract_active_minutes(response.json())}


@app.get("/activity_segment")
async def get_activity_segment():
    """Get user's activity segment data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.activity.segment:com.google.android.gms:merge_activity_segments/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"activity_segment": extract_activity_segment(response.json())}


@app.get("/bmr_calories")
async def get_bmr_calories():
    """Get user's BMR calories data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.calories.bmr:com.google.android.gms:merged/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"bmr_calories": extract_bmr_calories(response.json())}


@app.get("/expended_calories")
async def get_expended_calories():
    """Get user's expended calories data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"expended_calories": extract_bmr_calories(response.json())}


@app.get("/step_count")
async def get_step_count():
    """Get user's step count data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"step_count": extract_step_count(response.json())}


@app.get("/distance")
async def get_distance():
    """Get user's distance data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"distance": extract_distance(response.json())}


@app.get("/heart_minutes")
async def get_heart_minutes():
    """Get user's heart minutes data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}

    # Updated data source to com.google.android.apps.fitness
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/raw:com.google.heart_minutes:com.google.android.apps.fitness:user_input/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    print(response.json())

    return {"heart_minutes": extract_heart_minutes(response.json())}


@app.get("/speed")
async def get_speed():
    """Get user's speed data from Google Fit."""
    if 'credentials' not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}
    response = requests.get(
        'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.speed:com.google.android.gms:merge_speed/datasets/0-' +
        str(int(time.time() * 1e9)),
        headers=headers
    )
    return {"speed": extract_speed(response.json())}


def extract_weight_and_height(weight_data, height_data):
    """Extract weight and height from Google Fit data."""
    weight_value = weight_data.get('point', [{}])[0].get(
        'value', [{}])[0].get('fpVal', None)
    height_value = height_data.get('point', [{}])[0].get(
        'value', [{}])[0].get('fpVal', None)
    return weight_value, height_value


def extract_active_minutes(active_minutes_data):
    """Extract active minutes from Google Fit data."""
    return [point.get('value', [{}])[0].get('intVal', 0) for point in active_minutes_data.get('point', [])]


def extract_activity_segment(activity_segment_data):
    """Extract activity segments from Google Fit data."""
    return [point.get('value', [{}])[0].get('intVal', 0) for point in activity_segment_data.get('point', [])]


def extract_bmr_calories(calories_data):
    """Extract BMR calories from Google Fit data."""
    return [point.get('value', [{}])[0].get('fpVal', 0) for point in calories_data.get('point', [])]


def extract_step_count(step_count_data):
    """Extract step count from Google Fit data."""
    return [point.get('value', [{}])[0].get('intVal', 0) for point in step_count_data.get('point', [])]


def extract_distance(distance_data):
    """Extract distance from Google Fit data."""
    return [point.get('value', [{}])[0].get('fpVal', 0) for point in distance_data.get('point', [])]


def extract_heart_minutes(heart_minutes_data):
    """Extract heart minutes from Google Fit data."""
    return [point.get('value', [{}])[0].get('intVal', 0) for point in heart_minutes_data.get('point', [])]


def extract_speed(speed_data):
    """Extract speed from Google Fit data."""
    return [point.get('value', [{}])[0].get('fpVal', 0) for point in speed_data.get('point', [])]


def credentials_to_dict(credentials):
    """Convert Credentials object to a dictionary for session storage."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }


# Start the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
