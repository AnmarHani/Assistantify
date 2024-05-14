from typing import TYPE_CHECKING
from fastapi import Request
import openai
import base64
import io
import os
from pydub import AudioSegment
from gtts import gTTS
from dotenv import load_dotenv

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
    async def voice(request: Request):
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
            gpt_message = send_to_gpt(response.text)
        tts = gTTS(gpt_message, lang="en")  # Convert text to speech
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")
        tts.save("response.mp3")  # Save the speech audio into a file
        with open("response.mp3", "rb") as f:
            audio_response = base64.b64encode(f.read()).decode(
                "utf-8"
            )  # Encode the audio file to base64
        return {
            "response": audio_response,
            "system_message": gpt_message,
            "user_message": response.text,
        }


    @app.post("/chat")
    async def chat(request: Request):
        data = await request.json()
        message = data["message"]

        response = send_to_gpt(message)
        return {"response": response}

