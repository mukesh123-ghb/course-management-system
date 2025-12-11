from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user, require_role

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=schemas.Course)
def create_course(
    course: schemas.CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_role("teacher"))
):
    return crud.create_course(db, course)

@router.post("/modules", response_model=schemas.Module)
def create_module(
    module: schemas.ModuleCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_role("teacher"))
):
    return crud.create_module(db, module)

@router.post("/lessons", response_model=schemas.Lesson)
def create_lesson(
    lesson: schemas.LessonCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(require_role("teacher"))
):
    return crud.create_lesson(db, lesson)

@router.get("/", response_model=List[schemas.Course])
def list_courses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.list_courses(db)

@router.post("/{course_id}/enroll", response_model=schemas.Enrollment)
def enroll_in_course(
    course_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    enrollment = schemas.EnrollmentCreate(user_id=current_user.id, course_id=course_id)
    return crud.enroll_student(db, enrollment)
