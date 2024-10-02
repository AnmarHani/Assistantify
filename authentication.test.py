import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_gateway import app, get_db
from utils.database_utils import Base, User
from utils.authentication_utils import get_password_hash
from jose import jwt

# Set up a test database (in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # Create the test database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the test database tables after each test
    Base.metadata.drop_all(bind=engine)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_register_user():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "age": 25,
        "country": "USA"
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "User created successfully"
    assert "account_address" in json_data

def test_register_user_existing_email():
    # Create a user first
    db = TestingSessionLocal()
    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=hashed_password,
        age=25,
        country="USA",
        blockchain_account="0x43eB3A2Af4b2eC285FcaA58Fe912880F3a58154a",
    )
    db.add(user)
    db.commit()

    # Try to register with the same email
    user_data = {
        "username": "anotheruser",
        "email": "testuser@example.com",
        "password": "anotherpassword",
        "age": 30,
        "country": "UK"
    }

    response = client.post("/register", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username or email already exists"}

def test_login_user():
    # Create a user for login
    db = TestingSessionLocal()
    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=hashed_password,
        age=25,
        country="USA",
        blockchain_account="0x43eB3A2Af4b2eC285FcaA58Fe912880F3a58154a",
    )
    db.add(user)
    db.commit()

    # Test login with correct credentials
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"

def test_login_user_incorrect_password():
    # Create a user for login
    db = TestingSessionLocal()
    hashed_password = get_password_hash("testpassword")
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=hashed_password,
        age=25,
        country="USA",
        blockchain_account="0x43eB3A2Af4b2eC285FcaA58Fe912880F3a58154a",
    )
    db.add(user)
    db.commit()

    # Test login with incorrect password
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

