from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, auth
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user(db, int(payload.get("user_id")))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

router = APIRouter(prefix="/forum", tags=["Forum"])

@router.post("/", response_model=schemas.Forum)
def create_message(forum: schemas.ForumCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_forum_message(db, forum)

@router.get("/course/{course_id}", response_model=List[schemas.Forum])
def get_messages(course_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Forum).filter(models.Forum.course_id == course_id).all()
