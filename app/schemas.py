from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    batch: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    batch: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: str
    syllabus_url: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: int

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id: int
    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    content: str
    content_type: Optional[str] = None
    module_id: int

class LessonCreate(LessonBase):
    pass

class Lesson(LessonBase):
    id: int
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class Enrollment(EnrollmentCreate):
    id: int
    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str

class Notification(NotificationCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ForumCreate(BaseModel):
    course_id: int
    user_id: int
    message: str

class Forum(ForumCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- New Schemas ---

class QuizOptionBase(BaseModel):
    text: str
    is_correct: bool

class QuizOptionCreate(QuizOptionBase):
    pass

class QuizOption(QuizOptionBase):
    id: int
    question_id: int
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str
    question_type: str
    points: int = 1

class QuestionCreate(QuestionBase):
    options: List[QuizOptionCreate] = []

class Question(QuestionBase):
    id: int
    quiz_id: int
    options: List[QuizOption] = []
    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    module_id: int

class QuizCreate(QuizBase):
    questions: List[QuestionCreate] = []

class Quiz(QuizBase):
    id: int
    questions: List[Question] = []
    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: Optional[datetime] = None
    course_id: int

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    class Config:
        from_attributes = True

class SubmissionBase(BaseModel):
    content: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    assignment_id: Optional[int] = None
    quiz_id: Optional[int] = None

class SubmissionUpdate(BaseModel):
    score: float
    feedback: Optional[str] = None

class Submission(SubmissionBase):
    id: int
    user_id: int
    assignment_id: Optional[int]
    quiz_id: Optional[int]
    score: Optional[float]
    feedback: Optional[str]
    submitted_at: datetime
    class Config:
        from_attributes = True

class LessonProgressUpdate(BaseModel):
    completed: bool

class LessonProgress(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    completed: bool
    last_accessed: datetime
    class Config:
        from_attributes = True

class Certificate(BaseModel):
    id: int
    user_id: int
    course_id: int
    issued_at: datetime
    certificate_url: str
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    amount: float
    currency: str = "USD"
    transaction_id: str

class PaymentCreate(PaymentBase):
    user_id: int

class Payment(PaymentBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
