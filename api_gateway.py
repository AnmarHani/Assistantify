import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlite3 import IntegrityError
import requests

from ProcessingSystem.setup_processing_system import setup_processing_system
from RewardingSystem.setup_rewarding_system import setup_rewarding_system
from AnalyticsSystem.setup_analytics_system import setup_analytics_system
from IoTSystem.setup_iot_system import setup_iot_system
from ProfileSystem.setup_profile_system import setup_profile_system

from utils.fake_data_generator import insert_fake_data

from utils.constants import PORT, HOST, BASE_URL
from utils.database_utils import get_db, User
from utils.authentication_utils import (
    get_password_hash,
    get_current_user,
    authenticate_user,
    create_access_token,
)

import os
from dotenv import load_dotenv
load_dotenv()

class Message(BaseModel):
    message: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    age: int
    country: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if(os.getenv("BLOCKCHAIN_ENV") == "True"): setup_rewarding_system(app)
setup_processing_system(app)
setup_analytics_system(app)
setup_profile_system(app)
if(os.getenv("IOT_ENV") == "True"): setup_iot_system(app)

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

print("#############################")
print("-------WORKING SYSTEMS-------")
print(f"BLOCKCHAIN SYSTEM: {True if os.getenv('BLOCKCHAIN_ENV') == 'True' else False}")
print("PROCESSING SYSTEM: True")
print("ANALYTICS SYSTEM: True")
print("PROFILE SYSTEM: True")
print(f"IOT SYSTEM: {True if os.getenv('IOT_ENV') == 'True' else False}")
print(f"IS DEVELOPMENT?: {True if os.getenv('DEV') == 'True' else False}")
print("#############################")

@app.get("/")
async def main():
    return {"message": "Hello World"}

@app.post("/register", response_model=Message)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    
    if(os.getenv("BLOCKCHAIN_ENV") == "True"):
        blockchain_address = requests.get(
            f"{BASE_URL}/get_new_user_blockchain_account"
        ).text
    else:
        blockchain_address = "0x43eB3A2Af4b2eC285FcaA58Fe912880F3a58154a"
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        age=user.age,
        country=user.country,
        blockchain_account=blockchain_address,
    )

    db.add(db_user)

    try:
        db.commit()
        insert_fake_data(db, db_user.id, False)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    db.refresh(db_user)
    return {
        "message": "User created successfully",
        "account_address": blockchain_address,
    }


@app.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("api_gateway:app", port=PORT, host=HOST, reload=True if os.getenv('DEV') == "True" else False)
