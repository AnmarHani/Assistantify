from sqlalchemy.orm import Session
from utils.database_utils import User, Productivity, Finance, Health
import json


def finance_prompt(user, db: Session):
    user = db.query(User).filter(User.username == user.username).first()
    finance_data = db.query(Finance).filter(Finance.user_id == user.id).first()

    return json.dumps(
        {
            "user_id": finance_data.user_id,
            "income": finance_data.income,
            "expenses": finance_data.expenses,
            "savings": finance_data.savings,
            "investments": finance_data.investments,
            "debts": finance_data.debts,
            "credit_score": finance_data.credit_score,
            "financial_goals": finance_data.financial_goals,
            "monthly_budget": finance_data.monthly_budget,
        }
    )


def health_prompt(user, db: Session):
    user = db.query(User).filter(User.username == user.username).first()
    health_data = db.query(Health).filter(Health.user_id == user.id).all()

    return json.dumps(
        [
            {
                "user_id": h.user_id,
                "allergies": h.allergies,
                "daily_calorie": h.daily_calorie,
                "fav_food": h.fav_food,
                "weight": h.weight,
                "medical_conditions": h.medical_conditions,
                "avg_heart_beat": h.avg_heart_beat,
            }
            for h in health_data
        ]
    )


def productivity_prompt(user: str, db: Session):
    user = db.query(User).filter(User.username == user.username).first()

    productivity_data = (
        db.query(Productivity).filter(Productivity.user_id == user.id).first()
    )

    return json.dumps(
        {
            "user_id": productivity_data.user_id,
            "daily_tasks_completed": productivity_data.daily_tasks_completed,
            "weekly_tasks_completed": productivity_data.weekly_tasks_completed,
            "monthly_tasks_completed": productivity_data.monthly_tasks_completed,
            "hours_worked_daily": productivity_data.hours_worked_daily,
            "hours_worked_weekly": productivity_data.hours_worked_weekly,
            "hours_worked_monthly": productivity_data.hours_worked_monthly,
            "breaks_taken_daily": productivity_data.breaks_taken_daily,
            "breaks_taken_weekly": productivity_data.breaks_taken_weekly,
            "breaks_taken_monthly": productivity_data.breaks_taken_monthly,
        }
    )
