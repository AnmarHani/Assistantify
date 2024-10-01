from sqlalchemy import (
    DateTime,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./assistantify.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    age = Column(Integer)
    country = Column(String)
    health = relationship("Health", back_populates="user", uselist=False)

    finance = relationship("Finance", back_populates="user", uselist=False)
    productivity = relationship("Productivity", back_populates="user", uselist=False)
    blockchain_account = Column(String, unique=False, index=True)
    transactions = relationship("Transaction", back_populates="user")

class Health(Base):
    __tablename__ = "health"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    allergies = Column(String)
    daily_calorie = Column(Integer)
    fav_food = Column(String)
    weight = Column(Integer)
    medical_conditions = Column(String)
    avg_heart_beat = Column(Integer)

    user = relationship("User", back_populates="health")


class Finance(Base):
    __tablename__ = "finance"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    income = Column(Float)
    expenses = Column(Float)
    savings = Column(Float)
    investments = Column(Float)
    debts = Column(Float)
    credit_score = Column(Integer)
    financial_goals = Column(String)
    monthly_budget = Column(Float)
    user = relationship("User", back_populates="finance")


class Productivity(Base):
    __tablename__ = "productivity"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    daily_tasks_completed = Column(Integer)
    weekly_tasks_completed = Column(Integer)
    monthly_tasks_completed = Column(Integer)
    hours_worked_daily = Column(Float)
    hours_worked_weekly = Column(Float)
    hours_worked_monthly = Column(Float)
    breaks_taken_daily = Column(Integer)
    breaks_taken_weekly = Column(Integer)
    breaks_taken_monthly = Column(Integer)
    user = relationship("User", back_populates="productivity")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # E.g., 'income', 'expense'
    transaction_reason = Column(String, nullable=True)  # E.g., 'grocery', 'salary'
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    
Base.metadata.create_all(bind=engine)
