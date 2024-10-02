# profileSystem.py

from typing import Optional
from fastapi import FastAPI, Body, Depends, HTTPException
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from utils.authentication_utils import get_current_user
from utils.database_utils import get_db, User, Health, Finance, Productivity, Transaction

# Pydantic models for request and response data

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

# Define the missing Pydantic models

class HealthInfo(BaseModel):
    allergies: Optional[str]
    daily_calorie: Optional[int]
    fav_food: Optional[str]
    weight: Optional[int]
    medical_conditions: Optional[str]
    exercise_routine: Optional[str]
    rest_days: Optional[int]
    daily_steps: Optional[int]
    workout_hours: Optional[float]
    diet_choices: Optional[str]
    stress_quality: Optional[str]
    height: Optional[int]

class FinanceInfo(BaseModel):
    income: Optional[float]
    monthly_budget: Optional[float]
    debts: Optional[float]
    investments: Optional[float]
    expenses: Optional[float]
    savings: Optional[float]
    credit_score: Optional[int]
    financial_goals: Optional[str]

class ProductivityInfo(BaseModel):
    hours_worked_daily: Optional[float]
    breaks_taken_daily: Optional[int]
    # Add other fields if needed

class UserFullInfo(BaseModel):
    username: str
    email: str
    age: Optional[int]
    country: Optional[str]
    career: Optional[str]
    habit: Optional[str]
    health: Optional[HealthInfo]
    finance: Optional[FinanceInfo]
    productivity: Optional[ProductivityInfo]

def setup_profile_system(app):
    @app.post("/user/form", response_model=Message)
    def submit_form(
        form_data: FormData = Body(...),
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update User model with career and habit
        if form_data.career is not None:
            user.career = form_data.career
        if form_data.habit is not None:
            user.habit = form_data.habit
        db.add(user)
        
        # Update or create Health data
        health = db.query(Health).filter(Health.user_id == user.id).first()
        if not health:
            health = Health(user_id=user.id)
        health_fields = {
            'allergies': form_data.allergies,
            'daily_calorie': form_data.daily_calorie,
            'fav_food': form_data.fav_food,
            'weight': form_data.weight,
            'medical_conditions': form_data.medical_conditions,
            'exercise_routine': form_data.exercise_routine,
            'rest_days': form_data.rest_days,
            'daily_steps': form_data.daily_steps,
            'workout_hours': form_data.workout_hours,
            'diet_choices': form_data.diet_choices,
            'stress_quality': form_data.stress_quality,
            'height': form_data.height,
        }
        for key, value in health_fields.items():
            if value is not None:
                setattr(health, key, value)
        db.add(health)
        
        # Update or create Finance data
        finance = db.query(Finance).filter(Finance.user_id == user.id).first()
        if not finance:
            finance = Finance(user_id=user.id)
        finance_fields = {
            'income': form_data.income,
            'monthly_budget': form_data.monthly_budget,
            'debts': form_data.debts,
            'investments': form_data.investments,
        }
        for key, value in finance_fields.items():
            if value is not None:
                setattr(finance, key, value)
        db.add(finance)
        
        # Update or create Productivity data
        productivity = db.query(Productivity).filter(Productivity.user_id == user.id).first()
        if not productivity:
            productivity = Productivity(user_id=user.id)
        productivity_fields = {
            'hours_worked_daily': form_data.work_hours,
            'breaks_taken_daily': form_data.breaks,
        }
        for key, value in productivity_fields.items():
            if value is not None:
                setattr(productivity, key, value)
        db.add(productivity)
        
        try:
            db.commit()
            return {"message": "Form data saved successfully"}
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while saving data")

    # Endpoint to get full user information
    @app.get("/user/full_info", response_model=UserFullInfo)
    def get_user_full_info(
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Fetch related data using relationships
        health = user.health
        finance = user.finance
        productivity = user.productivity

        # Map SQLAlchemy models to Pydantic models
        health_info = None
        if health:
            health_info = HealthInfo(
                allergies=health.allergies,
                daily_calorie=health.daily_calorie,
                fav_food=health.fav_food,
                weight=health.weight,
                medical_conditions=health.medical_conditions,
                exercise_routine=health.exercise_routine,
                rest_days=health.rest_days,
                daily_steps=health.daily_steps,
                workout_hours=health.workout_hours,
                diet_choices=health.diet_choices,
                stress_quality=health.stress_quality,
                height=health.height,
            )

        finance_info = None
        if finance:
            finance_info = FinanceInfo(
                income=finance.income,
                monthly_budget=finance.monthly_budget,
                debts=finance.debts,
                investments=finance.investments,
                expenses=finance.expenses,
                savings=finance.savings,
                credit_score=finance.credit_score,
                financial_goals=finance.financial_goals,
            )

        productivity_info = None
        if productivity:
            productivity_info = ProductivityInfo(
                hours_worked_daily=productivity.hours_worked_daily,
                breaks_taken_daily=productivity.breaks_taken_daily,
                # Add other fields if needed
            )

        user_info = UserFullInfo(
            username=user.username,
            email=user.email,
            age=user.age,
            country=user.country,
            career=user.career,
            habit=user.habit,
            health=health_info,
            finance=finance_info,
            productivity=productivity_info,
        )
        return user_info

    # Endpoint to get user basic information
    @app.get("/user/info", response_model=UserBasicInfo)
    def get_user_info(
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_info = UserBasicInfo(
            username=user.username,
            email=user.email,
            age=user.age,
            country=user.country,
        )
        return user_info

    @app.put("/user/update", response_model=Message)
    def update_user_profile(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user),
    ):
        # Retrieve the User object from the database using the username
        user = db.query(User).filter(User.username == current_user).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Update only the fields that are provided
        if user_update.username is not None:
            user.username = user_update.username

        if user_update.email is not None:
            user.email = user_update.email

        if user_update.age is not None:
            user.age = user_update.age

        if user_update.country is not None:
            user.country = user_update.country

        db.add(user)

        try:
            db.commit()
            return {"message": "User profile updated successfully"}
        except IntegrityError as e:
            db.rollback()
            # Handle uniqueness constraint violations
            if 'UNIQUE constraint failed: users.username' in str(e.orig):
                raise HTTPException(status_code=400, detail="Username already exists")
            elif 'UNIQUE constraint failed: users.email' in str(e.orig):
                raise HTTPException(status_code=400, detail="Email already exists")
            else:
                raise HTTPException(status_code=500, detail="An error occurred while updating user profile")

    @app.post("/user/transaction", response_model=Message)
    def add_transaction(
        transaction: TransactionCreate,
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_transaction = Transaction(
            user_id=user.id,
            transaction_amount=transaction.transaction_amount,
            transaction_type=transaction.transaction_type,
            transaction_reason=transaction.transaction_reason,
        )

        db.add(new_transaction)
        db.commit()
        return {"message": "Transaction added successfully"}
