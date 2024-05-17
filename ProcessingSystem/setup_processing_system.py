import asyncio
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
from langdetect import detect
from pydub import AudioSegment
from sqlalchemy.orm import Session

from AnalyticsSystem.prompt_functions import (
    finance_prompt,
    health_prompt,
    productivity_prompt,
)
from utils.authentication_utils import get_current_user
from utils.constants import HOST, PORT
from utils.database_utils import User, get_db

if TYPE_CHECKING:
    from fastapi import FastAPI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = openai.OpenAI(api_key=OPENAI_API_KEY)


async def send_to_gpt(message: str, user, db: Session):
    content = f"""
        Your name is Assistantify (A Personal Assistant System), you are helping {user.username},
        with data: {finance_prompt(user, db)}, {health_prompt(user, db)}, {productivity_prompt(user, db)} in the financial, health, and productivity life domains respectively. 
        Any message will be based on this data, Give them helpful  advices, suggestions, and predictions them based on the message they have sent and their data that is given to you.
    """
    detected_language = detect(message)

    if (
        "clean" in message.lower()
        or "تنظيف" in message.lower()
        or "نظف" in message.lower()
        or "نظافة" in message.lower()
    ):
        async with httpx.AsyncClient() as client:
            await client.get(f"http://{HOST}:{PORT}/device_on")
        if detected_language == "ar": 
            return "ابشر، الان ببدا انظف!"
        return "Sure! I will start cleaning now."

    if (
        "back" in message.lower()
        or "رجوع" in message.lower()
        or "إرجعي" in message.lower()
        or "رجع" in message.lower()
    ):
        async with httpx.AsyncClient() as client:
            await client.get(f"http://{HOST}:{PORT}/device_off")
        if detected_language == "ar": 
            return "ان شاءالله نكون ادينا الواجب"
        return "Okay, Turning Off."

    if (
        "steps" in message.lower()
        or "achieve" in message.lower()
        or "apple" in message.lower()
        or "خطوات" in message.lower()
        or "خطوة" in message.lower()
        or "تفاح" in message.lower()
        or "إنجاز" in message.lower()
        or "نجزت" in message.lower()
    ):
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://{HOST}:{PORT}/reward_user",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"account_address": f"{user.blockchain_account}"}),
            )
        if (
            "5,000" in message.lower()
            or "خمسة" in message.lower()
            or "خمس" in message.lower()
        ):
            if detected_language == "ar": 
                return "ماشاءالله! إنجاز رِياضي مُمتاز! اكيد هذا الشيء بيحسن من صحتك.... وبعطيك جاظزة عُملة واحدة من ATN"
            return "Wow! You have Walked 5000 Steps, Here is 1 ATN Coin"
        elif (
            "ate" in message.lower()
            or "eat" in message.lower()
            or "اكل" in message.lower()
            or "أكل" in message.lower()
        ):
            if detected_language == "ar": 
                return "اختيار مُوَفِّق، اكْل التفاح يُعتبر شيء جيد لصحتك... وبعطيك جائزة عُملة واحدة من ATN"
            return "Nice Choice, Eating Apple is Healthy, Here is 1 ATN Coin"
        else:
            if detected_language == "ar": 
                return "انجازات اكثر من رائعة! نبغَى نسمع انجازات اكثر واكثر باذن الله، بعطيك جائزة على هذه الانجازات، عبارة عن عُملة واحدة من ATN"
            return "Wow! You have Achieved All This, Here is 1 ATN Coin"

    session = [
        {"role": "system", "content": content},
        {"role": "user", "content": message},
    ]
    print(session)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": msg["role"], "content": msg["content"]} for msg in session],
    )
    return response.choices[0].message.content


def setup_processing_system(app: "FastAPI"):
    @app.post("/voice")
    async def voice(
        request: Request,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
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

        user: User = db.query(User).filter(User.username == current_user).first()

        with open("temp.wav", "rb") as f:
            response = openai.audio.transcriptions.create(model="whisper-1", file=f)
            gpt_message = await send_to_gpt(response.text, user, db)


        tts_response = openai.audio.speech.create(
            model="tts-1",  # Choose the desired TTS model
            voice="onyx",  # Choose the voice (e.g., alloy, echo, fable, etc.)
            input=gpt_message,
        )

        # Save the speech audio into a file
        tts_response.stream_to_file("response.mp3")
        
        with open("response.mp3", "rb") as f:
            audio_response = base64.b64encode(f.read()).decode(
                "utf-8"
            )  # Encode the audio file to base64

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

        async with httpx.AsyncClient() as client:
            blockchain_balance = await client.post(
                f"http://{HOST}:{PORT}/get_account_balance",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"account_address": f"{user.blockchain_account}"}),
            )

        coins = blockchain_balance.text

        return {"response": response, "coins": coins}
