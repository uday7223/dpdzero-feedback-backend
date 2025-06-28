from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)

@router.post("/", response_model=schemas.FeedbackResponse)
def create_feedback(
    feedback: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    
    
    if current_user.role != models.RoleEnum.manager:
        raise HTTPException(status_code=403, detail="Only managers can create feedback")

    employee = db.query(models.User).filter(
    models.User.id == feedback.employee_id,
    models.User.role == models.RoleEnum.employee
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    if employee.manager_id != current_user.id:  
        raise HTTPException(status_code=403, detail="You can only give feedback to your own team members.")

    new_feedback = models.Feedback(
        manager_id=current_user.id,
        employee_id=feedback.employee_id,
        strengths=feedback.strengths,
        areas_to_improve=feedback.areas_to_improve,
        sentiment=feedback.sentiment
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@router.get("/employee", response_model=List[schemas.FeedbackResponse])
def get_my_feedback(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != models.RoleEnum.employee:
        raise HTTPException(status_code=403, detail="Only employees can view this")

    feedbacks = db.query(models.Feedback).filter(models.Feedback.employee_id == current_user.id).all()
    return feedbacks


@router.get("/team", response_model=List[schemas.FeedbackResponse])
def get_team_feedback(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role != models.RoleEnum.manager:
        raise HTTPException(status_code=403, detail="Only managers can view this")

    feedbacks = db.query(models.Feedback).filter(models.Feedback.manager_id == current_user.id).all()
    return feedbacks

@router.put("/{feedback_id}", response_model=schemas.FeedbackResponse)
def update_feedback(
    feedback_id: int,
    update_data: schemas.FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    feedback = db.query(models.Feedback).filter(
        models.Feedback.id == feedback_id,
        models.Feedback.manager_id == current_user.id
    ).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found or unauthorized")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(feedback, field, value)

    db.commit()
    db.refresh(feedback)
    return feedback


@router.put("/acknowledge/{feedback_id}")
def acknowledge_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    feedback = db.query(models.Feedback).filter(
        models.Feedback.id == feedback_id,
        models.Feedback.employee_id == current_user.id
    ).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found or unauthorized")

    feedback.acknowledged = True
    db.commit()
    return {"message": "Feedback acknowledged"}
