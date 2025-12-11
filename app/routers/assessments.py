from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user, require_role, require_admin

router = APIRouter(prefix="/assessments", tags=["Assessments"])

# --- Quizzes ---

@router.post("/modules/{module_id}/quizzes", response_model=schemas.Quiz)
def create_quiz(
    module_id: int, 
    quiz: schemas.QuizCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("teacher"))
):
    # Verify module exists?
    quiz.module_id = module_id
    return crud.create_quiz(db, quiz)

@router.get("/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(
    quiz_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

# --- Assignments ---
@router.post("/courses/{course_id}/assignments", response_model=schemas.Assignment)
def create_assignment(
    course_id: int,
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("teacher"))
):
    assignment.course_id = course_id
    return crud.create_assignment(db, assignment)

@router.get("/assignments/{assignment_id}", response_model=schemas.Assignment)
def read_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ass = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not ass:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return ass

# --- Submissions ---

@router.post("/submissions", response_model=schemas.Submission)
def submit_work(
    submission: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_submission(db, submission, current_user.id)

@router.put("/submissions/{submission_id}/grade", response_model=schemas.Submission)
def grade_submission(
    submission_id: int,
    grade: schemas.SubmissionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("teacher"))
):
    sub = crud.grade_submission(db, submission_id, grade)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub
