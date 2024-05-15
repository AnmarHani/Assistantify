from typing import TYPE_CHECKING
from fastapi import Request
from sqlalchemy.orm import Session
from utils.database_utils import User, get_db
from utils.authentication_utils import get_current_user

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_analytics_system(app: "FastAPI"):
    # System Prompts
    @app.get("/finance_prompt")
    def finance_prompt():
        return "Turned ON The Device"
