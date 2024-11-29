import time
import requests
from datetime import datetime


def send_atn_reward_request():
    try:
        response = requests.get("https://atn-reward-system.onrender.com")

        print(f"Request sent to ATN REWARD SYSTEM at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        
        print(f"An error occurred: {e}")
        
def send_api_gateway_request():
    try:
        response = requests.get("https://atn-api-gateway.onrender.com")

        print(f"Request sent to API GATEWAY SYSTEM at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

while True:
    send_api_gateway_request()
    send_atn_reward_request()
    time.sleep(5 * 60)