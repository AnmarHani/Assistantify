from sqlalchemy import DateTime, create_engine, Column, Integer, String, ForeignKey
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
    points = relationship("Points", back_populates="user")
    blockchain_account = Column(String, unique=False, index=True)


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


class Points(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    points = Column(Integer)
    date_time = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="points")


Base.metadata.create_all(bind=engine)
