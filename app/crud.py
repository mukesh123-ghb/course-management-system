from sqlalchemy.orm import Session
from app import models, schemas, auth
from datetime import datetime

# --- User Management ---

def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed, role=user.role, batch=user.batch)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, data: schemas.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    if data.password:
        user.hashed_password = auth.get_password_hash(data.password)
    for field, value in data.dict(exclude_unset=True).items():
        if field == "password": continue
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user

# --- Course Creation ---

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def list_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def create_module(db: Session, module: schemas.ModuleCreate):
    db_module = models.Module(**module.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

def create_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

# --- Enrollment & Community ---

def enroll_student(db: Session, enrollment: schemas.EnrollmentCreate):
    # Check if already enrolled
    existing = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.user_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    if existing:
        return existing
    
    db_enroll = models.Enrollment(student_id=enrollment.user_id, course_id=enrollment.course_id)
    db.add(db_enroll)
    db.commit()
    db.refresh(db_enroll)
    return db_enroll

def create_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def create_forum_message(db: Session, forum: schemas.ForumCreate):
    db_forum = models.Forum(**forum.dict())
    db.add(db_forum)
    db.commit()
    db.refresh(db_forum)
    return db_forum

# --- Assessments ---

def create_quiz(db: Session, quiz: schemas.QuizCreate):
    # Create Quiz Metadata
    db_quiz = models.Quiz(
        title=quiz.title, 
        description=quiz.description, 
        module_id=quiz.module_id
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    
    # Create Questions and Options
    for q in quiz.questions:
        db_question = models.Question(
            quiz_id=db_quiz.id,
            text=q.text,
            question_type=q.question_type,
            points=q.points
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        for opt in q.options:
            db_option = models.QuizOption(
                question_id=db_question.id,
                text=opt.text,
                is_correct=opt.is_correct
            )
            db.add(db_option)
        db.commit()
    
    return db_quiz

def create_assignment(db: Session, assignment: schemas.AssignmentCreate):
    db_assignment = models.Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def create_submission(db: Session, submission: schemas.SubmissionCreate, user_id: int):
    # Check if exists (optional, multiple submissions might be allowed)
    db_submission = models.Submission(
        user_id=user_id,
        assignment_id=submission.assignment_id,
        quiz_id=submission.quiz_id,
        content=submission.content
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def grade_submission(db: Session, submission_id: int, grade_data: schemas.SubmissionUpdate):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        return None
    submission.score = grade_data.score
    submission.feedback = grade_data.feedback
    db.commit()
    db.refresh(submission)
    return submission

# --- Tracking ---

def update_lesson_progress(db: Session, user_id: int, lesson_id: int, completed: bool):
    progress = db.query(models.LessonProgress).filter(
        models.LessonProgress.user_id == user_id,
        models.LessonProgress.lesson_id == lesson_id
    ).first()
    
    if progress:
        progress.completed = completed
        progress.last_accessed = datetime.utcnow()
    else:
        progress = models.LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            completed=completed
        )
        db.add(progress)
    
    db.commit()
    db.refresh(progress)
    return progress

def get_user_progress(db: Session, user_id: int):
    return db.query(models.LessonProgress).filter(models.LessonProgress.user_id == user_id).all()

def issue_certificate(db: Session, user_id: int, course_id: int, url: str):
    cert = models.Certificate(user_id=user_id, course_id=course_id, certificate_url=url)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

# --- Admin ---

def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.dict(), status="completed") # Mock status
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
