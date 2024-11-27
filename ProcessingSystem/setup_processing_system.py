import asyncio
import base64
import io
import json
import os
from typing import TYPE_CHECKING

import httpx
import openai
from dotenv import load_dotenv
from fastapi import Depends, Request, File, UploadFile, HTTPException, Form
# from fastapi.responses import FileResponse
# import requests
# from gtts import gTTS
# from langdetect import detect
from pydub import AudioSegment
from sqlalchemy.orm import Session

from AnalyticsSystem.prompt_functions import (
    finance_prompt,
    health_prompt,
    productivity_prompt,
)
from utils.authentication_utils import get_current_user
from utils.constants import GPT_MODEL, VOICE_MODEL, BASE_URL
from utils.database_utils import User, get_db, get_fake_coins, add_fake_coins

if TYPE_CHECKING:
    from fastapi import FastAPI

load_dotenv()
openai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_action(response_text: str, action_id: str):
    start = response_text.find(f'[{action_id}')
    end = response_text.find(']', start)

    if start != -1 and end != -1:
        extracted_str = response_text[start:end+1]
        
        cleaned_str = extracted_str.replace(f'[{action_id}, ', '').replace(']', '')
                
        entry_parts = [part.strip().strip('"') for part in cleaned_str.split(',')]

        return entry_parts
    else:
        return -1

async def send_to_gpt(message: str, user, db: Session):
    content = f"""
        Your name is Assistantify (A Personal Assistant System), you are helping {user.username},
        You will do one of two things, either 1. Answer (Suggestion, Prediction) Based on {user.username}'s data or 2. Action (Reward, Send Action From List)
        Actions list = [LIGHTS_ON, LIGHTS_OFF, REW_ATN, ADD_STOCK, REM_STOCK], You can only send a reward action based on {user.username} behaviour on their message, if they did good (Other Answers, or bad actions should be ignored as for rewarding action) based on the data, append to the message you will say You will get rewarded with 1 ATN (which is the Coin for rewards).
        Action Description: REW_ATN [REW_ATN, <ATN_VALUE>], ADD_STOCK [ADD_STOCK, <STOCK_NAME>, <STOCK_PRICE>, <STOCK_NUM>].
        When choosing an action (you can make multiple actions) based on user message or automatically, please write the action with the same format in the action description [ADD_STOCK, ..entries] or [REW_ATN, ..entries], I will read it from your response and extract the entries.
        with data: {finance_prompt(user, db)}, {health_prompt(user, db)}, {productivity_prompt(user, db)} in the financial, health, and productivity life domains respectively. 
        Any message will be based on this data, Give them helpful  advices, suggestions, and predictions them based on the message they have sent and their data that is given to you.
    """
    # detected_language = detect(message)

    session = [
        {"role": "system", "content": content},
        {"role": "user", "content": message},
    ]

    response = openai.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": msg["role"], "content": msg["content"]} for msg in session],
    )

    response_text = response.choices[0].message.content

    if "REW_ATN" in response_text:
        if os.getenv("BLOCKCHAIN_ENV") == "True":
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{BASE_URL}/reward_user",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"account_address": f"{user.blockchain_account}"}),
                )
        else:
            add_fake_coins()

    if "ADD_STOCK" in response_text:
        ACTION_ID = "ADD_STOCK"
        print(extract_action(response_text, ACTION_ID))

    return response_text


async def transcribe_audio(file_path: str):
    with open(file_path, "rb") as f:
        response = openai.audio.transcriptions.create(model="whisper-1", file=f)
    return response.text


async def text_to_voice(text: str):
    tts_response = openai.audio.speech.create(
        model=VOICE_MODEL,  # Choose the desired TTS model
        voice="onyx",  # Choose the voice (e.g., alloy, echo, fable, etc.)
        input=text,
    )

    # Save the speech audio into a file
    tts_response.write_to_file(os.path.join("static", "response.mp3"))

    return True


def setup_processing_system(app: "FastAPI"):

    @app.post("/file_upload_test")
    async def file_upload_test(
        file: UploadFile = File(...)
    ):

        file_bytes = await file.read(100)
        print(file_bytes)
        
        with open(os.path.join("static", file.filename), "wb") as f:
            while chunk := await file.read(1024):  # Read the file in chunks
                f.write(chunk)
        
        return {"message": f"Thank you for testing! The file name is: {file.filename} which can be accessed from: https://atn-api-gateway.onrender.com/code/static/{file.filename}"}

    @app.post("/vision")
    async def vision(
        message: str = Form(...),
        file: UploadFile = File(...),
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        # Read the uploaded image file
        file_bytes = await file.read()

        # Convert the image to base64
        base64_image = base64.b64encode(file_bytes).decode("utf-8")

        image_session = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ]

        image_response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": msg["role"], "content": msg["content"]}
                for msg in image_session
            ],
        )

        image_text = image_response.choices[0].message.content
        combined_message = str(message) + " " + "The Image is: " + image_text
        user: User = db.query(User).filter(User.username == current_user).first()
        gpt_response = await send_to_gpt(combined_message, user, db)

        if os.getenv("BLOCKCHAIN_ENV") == "True":
            async with httpx.AsyncClient() as client:
                blockchain_balance = await client.post(
                    f"{BASE_URL}/get_account_balance",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"account_address": f"{user.blockchain_account}"}),
                )

            coins = blockchain_balance.text
        else:
            coins = get_fake_coins()

        return {"bot_message": gpt_response, "coins": coins}

    @app.post("/voice")
    async def voice(
        file: UploadFile = File(...),
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        # Check if audio file is valid
        if file.content_type not in [
            "audio/3gp",
            "audio/caf",
            "audio/wav",
            "audio/mpeg",
            "audio/x-m4a",  # M4A support
            "audio/mp4",  # Sometimes M4A files have this content type
        ]:
            raise HTTPException(status_code=400, detail="Invalid audio format")

        # Read the uploaded file
        file_bytes = await file.read()

        audio_io = io.BytesIO(file_bytes)

        # Save the audio as a temporary WAV file
        audio = AudioSegment.from_file(audio_io)
        temp_wav_path = "temp.wav"
        audio.export(temp_wav_path, format="wav")

        # Step 1: Transcribe the audio using Whisper (assume transcribe_audio() is defined)
        voice_to_text = await transcribe_audio(temp_wav_path)

        user: User = db.query(User).filter(User.username == current_user).first()
        gpt_response = await send_to_gpt(voice_to_text, user, db)

        await text_to_voice(gpt_response)

        # Remove the temp wav file after processing
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

        if os.getenv("BLOCKCHAIN_ENV") == "True":
            async with httpx.AsyncClient() as client:
                blockchain_balance = await client.post(
                    f"{BASE_URL}/get_account_balance",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"account_address": f"{user.blockchain_account}"}),
                )

            coins = blockchain_balance.text
        else:
            coins = get_fake_coins()

        # Step 3: Return the mp3 file path as a response
        return {
            "file_path": f"https://atn-api-gateway.onrender.com/code/static/response.mp3",
            "bot_message": gpt_response,
            "user_message": voice_to_text,
            "coins": coins,
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
        response = await send_to_gpt(message, user, db)

        if os.getenv("BLOCKCHAIN_ENV") == "True":
            async with httpx.AsyncClient() as client:
                blockchain_balance = await client.post(
                    f"{BASE_URL}/get_account_balance",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"account_address": f"{user.blockchain_account}"}),
                )

            coins = blockchain_balance.text
        else:
            coins = get_fake_coins()

        return {"bot_message": response, "coins": coins}
