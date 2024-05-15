from sqlalchemy.orm import Session
from utils.database_utils import User, Productivity

def finance_prompt(user):
    return user

def health_prompt(user):
    return user

def productivity_prompt(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    productivity_data = db.query(Productivity).filter(Productivity.user_id == user.id).first()

    productivity_info = {
        "user_id": productivity_data.user_id,
        "daily_tasks_completed": productivity_data.daily_tasks_completed,
        "weekly_tasks_completed": productivity_data.weekly_tasks_completed,
        "monthly_tasks_completed": productivity_data.monthly_tasks_completed,
        "hours_worked_daily": productivity_data.hours_worked_daily,
        "hours_worked_weekly": productivity_data.hours_worked_weekly,
        "hours_worked_monthly": productivity_data.hours_worked_monthly,
        "breaks_taken_daily": productivity_data.breaks_taken_daily,
        "breaks_taken_weekly": productivity_data.breaks_taken_weekly,
        "breaks_taken_monthly": productivity_data.breaks_taken_monthly
    }

    return "Your name is Assistantify (A Personal Assistant System), you are helping {username} with data: {productivity_info} in the productivity life domain. Help them based on the message they have sent"