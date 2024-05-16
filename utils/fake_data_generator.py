import random

from faker import Faker
from sqlalchemy.orm import Session

from utils.database_utils import Finance, Health, Productivity

fake = Faker()

def generate_fake_data(user_id):
    # Generate fake data for Health table
    health_data = Health(
        user_id=user_id,
        allergies=fake.word(),
        daily_calorie=random.randint(1500, 2500),
        fav_food=fake.word(),
        weight=random.randint(50, 100),
        medical_conditions=fake.word(),
        avg_heart_beat=random.randint(60, 100)
    )

    # Generate fake data for Finance table
    finance_data = Finance(
        user_id=user_id,
        income=random.uniform(3000, 10000),
        expenses=random.uniform(1000, 5000),
        savings=random.uniform(500, 3000),
        investments=random.uniform(500, 3000),
        debts=random.uniform(0, 5000),
        credit_score=random.randint(300, 850),
        financial_goals=fake.sentence(),
        monthly_budget=random.uniform(1000, 5000)
    )

    # Generate fake data for Productivity table
    productivity_data = Productivity(
        user_id=user_id,
        daily_tasks_completed=random.randint(0, 10),
        weekly_tasks_completed=random.randint(0, 70),
        monthly_tasks_completed=random.randint(0, 300),
        hours_worked_daily=random.uniform(0, 24),
        hours_worked_weekly=random.uniform(0, 168),
        hours_worked_monthly=random.uniform(0, 720),
        breaks_taken_daily=random.randint(0, 10),
        breaks_taken_weekly=random.randint(0, 70),
        breaks_taken_monthly=random.randint(0, 300)
    )

    return health_data, finance_data, productivity_data


def insert_fake_data(db: Session, user_id: int):
    health_data, finance_data, productivity_data = generate_fake_data(user_id)
    
    db.add(health_data)
    db.add(finance_data)
    db.add(productivity_data)
    
    db.commit()