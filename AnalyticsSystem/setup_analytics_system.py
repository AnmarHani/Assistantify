import base64
from io import BytesIO
from typing import TYPE_CHECKING

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from utils.authentication_utils import get_current_user
from utils.database_utils import Finance, Health, Productivity, User, get_db

if TYPE_CHECKING:
    from fastapi import FastAPI


def generate_base64_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return img_base64


def calculate_tdee(weight, height=170, age=30, gender="male", activity_level=1.55):
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    tdee = bmr * activity_level
    return tdee


def setup_analytics_system(app: "FastAPI"):
    # System Prompts
    @app.get("/analysis", response_model=dict)
    def analysis(
        current_user: str = Depends(get_current_user), db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        productivity_data = (
            db.query(Productivity).filter(Productivity.user_id == user.id).first()
        )
        if not productivity_data:
            raise HTTPException(status_code=404, detail="Productivity data not found")

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        hours = list(range(24))
        tasks = np.random.randint(1, 10, size=(24, 7))

        fig, ax = plt.subplots(figsize=(12, 8))
        cax = ax.matshow(tasks.T, cmap="viridis")
        fig.colorbar(cax)

        ax.set_xticks(range(len(hours)))
        ax.set_xticklabels(hours, fontsize=12)
        ax.set_yticks(range(len(days)))
        ax.set_yticklabels(days, rotation=0, ha="right", fontsize=12)

        ax.set_xlabel("Hour of the Day", fontsize=14)
        ax.set_ylabel("Day of the Week", fontsize=14)
        ax.set_title("Productivity Analysis", fontsize=16)

        ax.grid(which="both", color="gray", linestyle="-", linewidth=0.5)
        fig.tight_layout()

        productivity_img = generate_base64_image(fig)

        finance_data = db.query(Finance).filter(Finance.user_id == user.id).first()
        if not finance_data:
            raise HTTPException(status_code=404, detail="Finance data not found")

        labels = ["Expenses", "Savings", "Investments", "Debts"]
        values = [
            finance_data.expenses,
            finance_data.savings,
            finance_data.investments,
            finance_data.debts,
        ]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_title("Finance Analysis")

        finance_img = generate_base64_image(fig)

        health_data = db.query(Health).filter(Health.user_id == user.id).all()
        if not health_data:
            raise HTTPException(status_code=404, detail="Health data not found")

        data = pd.DataFrame(
            [
                {"daily_calorie": h.daily_calorie, "weight": h.weight}
                for h in health_data
            ]
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(x="daily_calorie", y="weight", data=data, ax=ax)
        ax.set_title("Daily Calorie Intake vs Weight")
        ax.set_xlabel("Daily Calorie Intake")
        ax.set_ylabel("Weight")

        for index, row in data.iterrows():
            weight = row["weight"]
            daily_calorie = row["daily_calorie"]
            tdee = calculate_tdee(weight)
            if daily_calorie > tdee:
                text = "Gain Weight"
                color = "red"
            else:
                text = "Lose Weight"
                color = "green"
            ax.text(
                daily_calorie,
                weight,
                text,
                horizontalalignment="left",
                size="medium",
                color=color,
                weight="semibold",
            )

        health_img = generate_base64_image(fig)

        return {"images": [health_img, productivity_img, finance_img]}
