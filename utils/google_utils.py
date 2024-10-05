from fastapi import FastAPI, Depends, HTTPException, Request, status
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
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.body.write',
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.activity.write',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.write'
]

# In-memory session for demonstration; use a proper session management system in production
session = {}


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


def get_credentials():
    """Retrieve credentials from session."""
    if 'credentials' not in session:
        raise HTTPException(
            status_code=401, detail="Unauthorized. Please authorize.")
    return Credentials(**session['credentials'])


def fetch_fit_data(data_source):
    """Fetch data from Google Fit API."""
    credentials = get_credentials()
    headers = {'Authorization': f'Bearer {credentials.token}'}

    now = int(time.time() * 1e9)
    all_the_time = 0  # Get all data

    response = requests.get(
        f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{data_source}/datasets/{int(all_the_time)}-{int(now)}',
        headers=headers
    )
    return response


@app.get("/fit_data", response_class=HTMLResponse)
async def get_user_fit_data(request: Request):
    """Fetch and display user fitness data."""
    if 'credentials' not in session:
        return RedirectResponse(url='/authorize')

    credentials = Credentials(**session['credentials'])
    headers = {'Authorization': f'Bearer {credentials.token}'}

    now = int(time.time() * 1e9)
    all_the_time = 0  # Get all data

    # Data sources used to fetch the data from Google Fit API
    data_sources = {
        'weight': 'derived:com.google.weight:com.google.android.gms:merge_weight',
        'height': 'derived:com.google.height:com.google.android.gms:merge_height',
        'bmr_calories': 'derived:com.google.calories.bmr:com.google.android.gms:merged',
        'step_count': 'derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas',
        'distance': 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',
        'heart_rate': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm',
    }

    print(get_fit_data_as_string())

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
        fit_data = {key: response.json().get('point', [])
                    for key, response in responses.items()}
        return fit_data


def handle_response(response):
    """Handle the response from Google Fit API."""
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code,
                            detail=response.json())


def credentials_to_dict(credentials):
    """Convert credentials to a dictionary."""
    print(f"token: {credentials.token} \nrefresh_token: {credentials.refresh_token} \ntoken_uri: {credentials.token_uri} \nclient_id: {credentials.client_id} \nclient_secret: {credentials.client_secret} \nscopes: {credentials.scopes}")
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


def get_fit_data_as_string():
    """Fetch user fitness data and return as string."""
    data_sources = {
        'weight': 'derived:com.google.weight:com.google.android.gms:merge_weight',
        'height': 'derived:com.google.height:com.google.android.gms:merge_height',
        'bmr_calories': 'derived:com.google.calories.bmr:com.google.android.gms:merged',
        'step_count': 'derived:com.google.step_count.delta:com.google.android.gms:merge_step_deltas',
        'distance': 'derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta',
        'heart_rate': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm'
    }

    # Fetch data and return only the last element if multiple exist
    fit_data = {}
    for key, data_source in data_sources.items():
        data = fetch_fit_data(data_source)
        data = data.json().get('point', [])
        if data:
            last_data = data[-1]  # Get the last element
            # Extract the fpVal or intVal depending on the data type
            if 'value' in last_data and last_data['value']:
                if 'fpVal' in last_data['value'][0]:
                    fit_data[key] = last_data['value'][0]['fpVal']
                elif 'intVal' in last_data['value'][0]:
                    fit_data[key] = last_data['value'][0]['intVal']
                else:
                    fit_data[key] = "Value not found"
            else:
                fit_data[key] = "Value not found"
        else:
            fit_data[key] = "No data"

    # Return formatted string with the last data points
    return f"""
Weight: {fit_data['weight']}
Height: {fit_data['height']}
BMR Calories: {fit_data['bmr_calories']}
Step Count: {fit_data['step_count']}
Distance: {fit_data['distance']}
Heart Rate: {fit_data['heart_rate']}
"""


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
