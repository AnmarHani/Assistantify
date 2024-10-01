# import netifaces
# HOST = netifaces.ifaddresses('en0')[2][0]["addr"]
import os
from dotenv import load_dotenv
load_dotenv()
HOST = "0.0.0.0"
PORT = 8080
BASE_URL = os.getenv("BASE_URL")
GPT_MODEL="gpt-4o-mini"
VOICE_MODEL="tts-1"