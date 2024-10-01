# profileSystem.py

from sqlite3 import IntegrityError
from fastapi import Body, Depends, HTTPException
from sqlalchemy.orm import Session
import sqlalchemy.exc
from typing import Optional
from utils.authentication_utils import get_current_user
from utils.database_utils import get_db, User, Health, Finance, Productivity
from utils.database_utils import get_db, User, Transaction

from ProfileSystem.utils.models import Message, FormData, UserBasicInfo, UserUpdate, TransactionCreate

def setup_profile_system(app):
    # Endpoint to handle form submission and save data
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
        except sqlalchemy.exc.SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while saving data")
    
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
        current_user: str = Depends(get_current_user),  # current_user is the username (str)
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
            

    @app.post("/user/transaction")
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