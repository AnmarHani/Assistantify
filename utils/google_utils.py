import requests
import time


def fetch_fit_data(data_source, access_token):
    """Fetch data from Google Fit API."""
    headers = {'Authorization': f'Bearer {access_token}'}

    now = int(time.time() * 1e9)
    all_the_time = 0  # Get all data

    response = requests.get(
        f'https://www.googleapis.com/fitness/v1/users/me/dataSources/{data_source}/datasets/{int(all_the_time)}-{int(now)}',
        headers=headers
    )
    return response


def get_fit_data_as_string(access_token):
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
        data = fetch_fit_data(data_source, access_token)
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


print(get_fit_data_as_string('ya29.a0AcM612y1AXUTJkmUVCWl0exGyV8E2GMqAwd7BVPQuxUAfF_72MiWE-J10zjTysMSSLm2gVIo5fju8czRWaQB8Nrk8XnCyrraMRrLJq5i3nv2oesF-QDFHQL236eiemFrNodddTArnENUoLXyGEkERjxzyOiSompSJVzB8lvdaCgYKAcoSARASFQHGX2MiddjF3QwqnttUnsAr_lLAoA0175'))
