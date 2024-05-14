from typing import Optional

from fastapi import Body, Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import sqlalchemy.exc


from utils.authentication_utils import get_current_user
from utils.database_utils import get_db, User, Health


class Message(BaseModel):
    message: str


class HealthProfile(BaseModel):
    allergies: Optional[str]
    daily_calorie: int
    fav_food: str
    weight: int
    medical_conditions: Optional[str]
    avg_heart_beat: int


class UserHealthProfile(BaseModel):
    username: str
    email: str
    age: int
    country: str
    health: HealthProfile


class FoodItem(BaseModel):
    food: str


class HealthData(BaseModel):
    allergies: str = Field(None, example="Pollen")
    daily_calorie: int = Field(..., gt=0, example=2500)
    fav_food: str = Field(..., example="Pizza")
    weight: int = Field(..., gt=0, example=70)
    medical_conditions: str = Field(None, example="None")
    avg_heart_beat: int = Field(..., gt=0, example=72)


def setup_analytics_system(app: "FastAPI"):
    # this endpoint is used to get the user information from the database
    @app.get("/get/user/health", response_model=UserHealthProfile)
    def get_user_health_profile(
        current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        health_data = db.query(Health).filter(Health.user_id == user.id).first()
        if not health_data:
            raise HTTPException(status_code=404, detail="Health data not found")

        user_health_profile = UserHealthProfile(
            username=user.username,
            email=user.email,
            age=user.age,
            country=user.country,
            health=HealthProfile(
                allergies=health_data.allergies,
                daily_calorie=health_data.daily_calorie,
                fav_food=health_data.fav_food,
                weight=health_data.weight,
                medical_conditions=health_data.medical_conditions,
                avg_heart_beat=health_data.avg_heart_beat,
            ),
        )
        return user_health_profile

    # this endpoint is used to insert the user health data into the database
    @app.post("/user/health", response_model=None)
    def insert_health_data(
        health_data: HealthData = Body(...),
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            new_health = Health(
                user_id=user.id,
                allergies=health_data.allergies,
                daily_calorie=health_data.daily_calorie,
                fav_food=health_data.fav_food,
                weight=health_data.weight,
                medical_conditions=health_data.medical_conditions,
                avg_heart_beat=health_data.avg_heart_beat,
            )
            db.add(new_health)
            db.commit()
            return {"message": "Health data added successfully"}
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Health data already exists for this user"
            )

    @app.post("/check_allergies", response_model=Message)
    def check_allergies(
        food_item: FoodItem,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        health_data = db.query(Health).filter(Health.user_id == user.id).first()
        if not health_data:
            raise HTTPException(status_code=404, detail="Health data not found")

        allergies = health_data.allergies.split(",")

        if food_item.food.lower() in [allergy.strip().lower() for allergy in allergies]:
            return {"message": "Alert: You are allergic to this food!"}
        else:
            return {"message": "No allergies detected for this food."}
