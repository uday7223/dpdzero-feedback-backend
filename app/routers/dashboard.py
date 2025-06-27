from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import get_current_user
from app import models
from typing import List
from collections import Counter
from app.models import RoleEnum


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Manager Dashboard: See feedback count and sentiment trends for each employee
@router.get("/manager")
def get_manager_dashboard(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    if current_user.role != RoleEnum.manager:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


    # Get all team members and their feedback
    employees = db.query(models.User).filter(models.User.manager_id == current_user.id).all()

    dashboard_data = []
    for emp in employees:
        feedbacks = db.query(models.Feedback).filter(models.Feedback.employee_id == emp.id).all()
        sentiments = [fb.sentiment for fb in feedbacks]
        sentiment_count = dict(Counter(sentiments))

        dashboard_data.append({
            "employee_id": emp.id,
            "employee_name": emp.username,
            "feedback_count": len(feedbacks),
            "sentiment_breakdown": sentiment_count
        })

    return dashboard_data


# Employee Dashboard: Timeline of feedbacks
@router.get("/employee")
def get_employee_dashboard(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != RoleEnum.employee:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


    feedbacks = db.query(models.Feedback).filter(models.Feedback.employee_id == current_user.id).order_by(models.Feedback.id.desc()).all()

    return feedbacks
