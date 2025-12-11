from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, users, courses, lessons, notifications, forum, assessments, tracking, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Management System")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(assessments.router)
app.include_router(tracking.router)
app.include_router(notifications.router)
app.include_router(forum.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Course Management System API"}
