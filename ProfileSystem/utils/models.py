from pydantic import BaseModel, Field, EmailStr, field_validator, validator
from typing import Optional


class Message(BaseModel):
    message: str

# Model for the form data
class FormData(BaseModel):
    # Personal Improvement
    career: Optional[str] = Field(None, example="Software Developer")
    work_hours: Optional[float] = Field(None, example=8)
    breaks: Optional[int] = Field(None, example=2)
    
    # Fitness
    exercise_routine: Optional[str] = Field(None, example="Running")
    rest_days: Optional[int] = Field(None, example=2)
    daily_steps: Optional[int] = Field(None, example=10000)
    workout_hours: Optional[float] = Field(None, example=1.5)
    
    # Nutrition
    diet_choices: Optional[str] = Field(None, example="Vegetarian")
    allergies: Optional[str] = Field(None, example="Peanuts")
    daily_calorie: Optional[int] = Field(None, example=2000)
    fav_food: Optional[str] = Field(None, example="Pasta")
    
    # Habit
    habit: Optional[str] = Field(None, example="Reading")
    
    # Medicine
    medical_conditions: Optional[str] = Field(None, example="None")
    stress_quality: Optional[str] = Field(None, example="Low")
    height: Optional[int] = Field(None, example=175)
    weight: Optional[int] = Field(None, example=70)
    
    # Finance
    income: Optional[float] = Field(None, example=5000)
    monthly_budget: Optional[float] = Field(None, example=3000)
    debts: Optional[float] = Field(None, example=1000)
    investments: Optional[float] = Field(None, example=2000)

class UserBasicInfo(BaseModel):
    username: str
    email: str
    age: Optional[int]
    country: Optional[str]

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    country: Optional[str] = None


class TransactionCreate(BaseModel):
    transaction_amount: float
    transaction_type: str  # e.g., 'income' or 'expense'
    transaction_reason: str