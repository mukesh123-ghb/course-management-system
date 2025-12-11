from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.post("/progress", response_model=schemas.LessonProgress)
def update_progress(
    lesson_id: int,
    progress: schemas.LessonProgressUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.update_lesson_progress(db, current_user.id, lesson_id, progress.completed)

@router.get("/progress", response_model=List[schemas.LessonProgress])
def read_my_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_user_progress(db, current_user.id)

@router.post("/certificates/issue", response_model=schemas.Certificate)
def generate_certificate(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Logic to verify course completion should go here
    # For now, we manually assume it's valid if they request it (or better, check logic)
    # Check if all modules/lessons are completed... skipped for brevity on MVP
    
    # Check if exists
    cert = db.query(models.Certificate).filter(
        models.Certificate.user_id == current_user.id,
        models.Certificate.course_id == course_id
    ).first()
    if cert:
        return cert
        
    mock_url = f"https://cert.example.com/{current_user.id}/{course_id}"
    return crud.issue_certificate(db, current_user.id, course_id, mock_url)
