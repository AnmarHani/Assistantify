import json
import os
from typing import TYPE_CHECKING
import httpx
import numpy as np
from openai import BaseModel
import pandas as pd
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from utils.authentication_utils import get_current_user
from utils.constants import BASE_URL
from utils.database_utils import Finance, Health, Productivity, User, get_db
from utils.database_utils import get_db, Transaction, User

class ChartResponse(BaseModel):
    x: list[int]  # Days
    y: list[float]  # Coins
if TYPE_CHECKING:
    from fastapi import FastAPI

def calculate_tdee(weight, height=170, age=30, gender="male", activity_level=1.55):
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    tdee = bmr * activity_level
    return tdee

def format_productivity_data(tasks, hours, days):
    """Helper function to format productivity data for cleaner JSON."""
    formatted_data = {}
    for day_index, day in enumerate(days):
        day_data = {}
        for hour_index, hour in enumerate(hours):
            # Convert numpy types to native Python types (e.g., np.int32 to int)
            day_data[f"{hour:02d}:00"] = int(tasks[hour_index][day_index])
        formatted_data[day] = day_data
    return formatted_data

def setup_analytics_system(app: "FastAPI"):
    @app.get("/all_analysis", response_model=dict)
    def analysis(
        current_user: str = Depends(get_current_user), 
        db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetching productivity data
        productivity_data = db.query(Productivity).filter(Productivity.user_id == user.id).first()
        if not productivity_data:
            raise HTTPException(status_code=404, detail="Productivity data not found")

        # Format productivity data with x and y values
        productivity_analysis = {
            "tasks_completed": {
                "x": ["Daily", "Weekly", "Monthly"],
                "y": [
                    productivity_data.daily_tasks_completed,
                    productivity_data.weekly_tasks_completed,
                    productivity_data.monthly_tasks_completed
                ]
            },
            "hours_worked": {
                "x": ["Daily", "Weekly", "Monthly"],
                "y": [
                    productivity_data.hours_worked_daily,
                    productivity_data.hours_worked_weekly,
                    productivity_data.hours_worked_monthly
                ]
            },
            "breaks_taken": {
                "x": ["Daily", "Weekly", "Monthly"],
                "y": [
                    productivity_data.breaks_taken_daily,
                    productivity_data.breaks_taken_weekly,
                    productivity_data.breaks_taken_monthly
                ]
            }
        }

        # Fetching finance data
        finance_data = db.query(Finance).filter(Finance.user_id == user.id).first()
        if not finance_data:
            raise HTTPException(status_code=404, detail="Finance data not found")

        finance_analysis = {
            "finance_breakdown": {
                "x": ["Income", "Expenses", "Savings", "Investments", "Debts"],
                "y": [
                    float(finance_data.income),
                    float(finance_data.expenses),
                    float(finance_data.savings),
                    float(finance_data.investments),
                    float(finance_data.debts)
                ]
            }
        }

        # Fetching health data
        health_data = db.query(Health).filter(Health.user_id == user.id).all()
        if not health_data:
            raise HTTPException(status_code=404, detail="Health data not found")

        # Assuming health_data has multiple entries over time
        dates = [record.timestamp.strftime("%Y-%m-%d") for record in health_data]
        weights = [float(record.weight) for record in health_data]
        daily_calories = [float(record.daily_calorie) for record in health_data]

        health_analysis = {
            "weight_over_time": {
                "x": dates,
                "y": weights
            },
            "calories_over_time": {
                "x": dates,
                "y": daily_calories
            }
        }

        # Returning a clean and structured JSON format
        return {
            "productivity_analysis": productivity_analysis,
            "finance_analysis": finance_analysis,
            "health_analysis": health_analysis,
        }
    @app.get("/user/transactions/analysis")
    def analyze_transactions(
        current_user: str = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Fetch all transactions related to the user
        transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()

        # Normalize transaction types to handle possible typos or variations
        total_income = sum(
            t.transaction_amount for t in transactions if t.transaction_type.lower() == "deposit"
        )
        total_expenses = sum(
            t.transaction_amount for t in transactions if t.transaction_type.lower() == "withdraw"
        )

        # Categorized income and expenses
        categorized_expenses = {}
        categorized_income = {}

        # Counters for transaction types
        withdraw_count = 0
        deposit_count = 0

        for t in transactions:
            if t.transaction_type.lower() == "withdraw":  # Normalize to lowercase
                withdraw_count += 1
                if t.transaction_reason not in categorized_expenses:
                    categorized_expenses[t.transaction_reason] = 0
                categorized_expenses[t.transaction_reason] += t.transaction_amount
            elif t.transaction_type.lower() == "deposit":  # Normalize to lowercase
                deposit_count += 1
                if t.transaction_reason not in categorized_income:
                    categorized_income[t.transaction_reason] = 0
                categorized_income[t.transaction_reason] += t.transaction_amount

        # Calculate the percentage of withdraw and deposit transactions
        total_transactions = withdraw_count + deposit_count
        if total_transactions > 0:
            withdraw_percentage = (withdraw_count / total_transactions) * 100
            deposit_percentage = (deposit_count / total_transactions) * 100
        else:
            withdraw_percentage = 0
            deposit_percentage = 0

        # Prepare response with all transactions
        all_transactions = [
            {
                "transaction_amount": t.transaction_amount,
                "transaction_type": t.transaction_type,
                "transaction_reason": t.transaction_reason,
                "timestamp": t.timestamp,
            }
            for t in transactions
        ]

        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_savings": total_income - total_expenses,
            "withdraw_percentage": withdraw_percentage,
            "deposit_percentage": deposit_percentage,
            "categorized_expenses": categorized_expenses,
            "categorized_income": categorized_income,
            "all_transactions": all_transactions,
        }


    @app.get("/general_analysis", response_model=ChartResponse)
    async def get_real_atn_chart(
        current_user: User = Depends(get_current_user), 
        db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Simulate Blockchain check
        if os.getenv("BLOCKCHAIN_ENV") == "True":
            async with httpx.AsyncClient() as client:
                blockchain_balance = await client.post(
                    f"{BASE_URL}/get_account_balance",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"account_address": user.blockchain_account}),
                )
            coins = float(blockchain_balance.text)
        else:
            coins = 0

        # Fake chart logic
        days = int(coins / 2)
        x = list(range(1, days + 1))  # Array of days
        y = [i * 2 for i in x]  # Array of coins

        return {"x": x, "y": y}

