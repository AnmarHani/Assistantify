import random

from faker import Faker
from sqlalchemy.orm import Session

from utils.database_utils import Finance, Health, Productivity, Transaction
import datetime

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
def generate_real_data(user_id):
    # Generate fake data for Health table
    real_health_data = Health(
        user_id=user_id,
        allergies="['Lactose', 'Milk', 'Peanut butter', 'Shrimp']",
        daily_calorie=random.randint(2000, 3200),
        fav_food='Burger, Pizza, Chicken with Rice (Saudi Arabian Kabsa)',
        weight=random.randint(50, 100),
        medical_conditions='Lactose Intolerance',
        avg_heart_beat=random.randint(70, 100)
    )

    # Generate fake data for Finance table
    real_finance_data = Finance(
        user_id=user_id,
        income=random.uniform(3000, 20000),
        expenses=random.uniform(1000, 5000),
        savings=random.uniform(500, 4000),
        investments=random.uniform(500, 4000),
        debts=random.uniform(0, 2500),
        credit_score=random.randint(300, 850),
        financial_goals="['Buying 1 million priced House in 10 Years, Buying a 500K priced Car in 12 Years']",
        monthly_budget=random.uniform(1000, 5000)
    )

    # Generate fake data for Productivity table
    real_productivity_data = Productivity(
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

    return real_health_data, real_finance_data, real_productivity_data


def generate_real_data_ziyad(user_id):
    real_health_data = Health(
        user_id=user_id,
        allergies="['Lactose']",
        daily_calorie=2500,  
        fav_food='Burger, Pizza, Chicken with Rice (Saudi Arabian Kabsa)',
        weight=82,  
        medical_conditions='Lactose Intolerance',
        avg_heart_beat=80,
        exercise_routine="Push Pull Legs",  # Updated exercise routine
        rest_days=2,  # 2 days of rest per week
        daily_steps=10000,  # Assuming 10,000 steps per day
        workout_hours=1.5,  # Average workout duration in hours
        diet_choices="High protein, moderate carbs, low lactose",  # Diet preference
        stress_quality="Low",  # Stress level
        height=175  # Assuming height in cm
    )


    real_finance_data = Finance(
        user_id=user_id,
        income=990,  
        expenses=200,  
        savings=790,  
        investments=50,  
        debts=0,  
        credit_score=700,  
        financial_goals="['Saving to buy a house']",
        monthly_budget=990  
    )

   
    real_productivity_data = Productivity(
        user_id=user_id,
        daily_tasks_completed=5,  
        weekly_tasks_completed=25,  
        monthly_tasks_completed=100,  
        hours_worked_daily=8,  
        hours_worked_weekly=40,  
        hours_worked_monthly=160,  
        breaks_taken_daily=2,  
        breaks_taken_weekly=10,  
        breaks_taken_monthly=40  
    )

   
    real_transaction_data = [
        Transaction(
            user_id=user_id,
            transaction_amount=50.0,
            transaction_type='expense',
            transaction_reason='Groceries',
            timestamp=datetime.datetime.utcnow()
        ),
        Transaction(
            user_id=user_id,
            transaction_amount=200.0,
            transaction_type='income',
            transaction_reason='Salary',
            timestamp=datetime.datetime.utcnow()
        ),
        Transaction(
            user_id=user_id,
            transaction_amount=15.0,
            transaction_type='expense',
            transaction_reason='Transportation',
            timestamp=datetime.datetime.utcnow()
        ),
        Transaction(
            user_id=user_id,
            transaction_amount=30.0,
            transaction_type='expense',
            transaction_reason='Dining Out',
            timestamp=datetime.datetime.utcnow()
        ),
        Transaction(
            user_id=user_id,
            transaction_amount=100.0,
            transaction_type='income',
            transaction_reason='Freelance Work',
            timestamp=datetime.datetime.utcnow()
        ),
    ]

    return real_health_data, real_finance_data, real_productivity_data, real_transaction_data

def insert_fake_data(db: Session, user_id: int, fake: bool = True):
    if fake:
        health_data, finance_data, productivity_data = generate_fake_data(user_id)
        db.add(health_data)
        db.add(finance_data)
        db.add(productivity_data)
        db.commit()
        return
    
    real_health_data, real_finance_data, real_productivity_data, real_transaction_data = generate_real_data_ziyad(user_id)
    db.add(real_health_data)
    db.add(real_finance_data)
    db.add(real_productivity_data)
    for transaction in real_transaction_data:
        db.add(transaction)
    db.commit()
    