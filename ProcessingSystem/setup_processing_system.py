import base64
import io
import json
import os
from typing import TYPE_CHECKING
import httpx
import openai
import requests
from dotenv import load_dotenv
from fastapi import Depends, Request
from gtts import gTTS
from pydub import AudioSegment
from sqlalchemy.orm import Session
import asyncio

from utils.authentication_utils import get_current_user
from utils.constants import HOST, PORT
from utils.database_utils import User, get_db


if TYPE_CHECKING:
    from fastapi import FastAPI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = openai.OpenAI(api_key=OPENAI_API_KEY)


def send_to_gpt(message: str):
    session = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": msg["role"], "content": msg["content"]} for msg in session],
    )
    return response.choices[0].message.content


def setup_processing_system(app: "FastAPI"):
    @app.post("/voice")
    async def voice(request: Request, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
        data = await request.json()
        file = data["file"]
        
        audio_file = base64.b64decode(file)
        audio_io = io.BytesIO(audio_file)
        audio_io.seek(0)
        
        # I Installed brew install ffmpeg "only" for this project, please work.
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")
        audio = AudioSegment.from_file(audio_io, format="3gp")  # or "caf" for iOS
        audio.export("temp.wav", format="wav")
        
        with open("temp.wav", "rb") as f:
            response = openai.audio.transcriptions.create(model="whisper-1", file=f)
            if 
            gpt_message = send_to_gpt(response.text)
        
        tts = gTTS(gpt_message, lang="en")  # Convert text to speech
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")
        tts.save("response.mp3")  # Save the speech audio into a file
        
        with open("response.mp3", "rb") as f:
            audio_response = base64.b64encode(f.read()).decode(
                "utf-8"
            )  # Encode the audio file to base64
        
        user: User = db.query(User).filter(User.username == current_user).first()
        
        async with httpx.AsyncClient() as client:
            blockchain_balance = await client.post(
                f"http://{HOST}:{PORT}/get_account_balance",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"account_address": f"{user.blockchain_account}"}),
            )
            
        coins = blockchain_balance.text
        
        return {
            "response": audio_response,
            "system_message": gpt_message,
            "user_message": response.text,
            "coins": coins
        }

    @app.post("/chat")
    async def chat(
        request: Request,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        data = await request.json()
        message = data["message"]

        user: User = db.query(User).filter(User.username == current_user).first()
        response = send_to_gpt(message)
        
        async with httpx.AsyncClient() as client:
            blockchain_balance = await client.post(
                f"http://{HOST}:{PORT}/get_account_balance",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"account_address": f"{user.blockchain_account}"}),
            )
            
        coins = blockchain_balance.text
            
        return {"response": response, "coins": coins}
