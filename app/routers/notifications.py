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

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=schemas.Notification)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(lambda: get_current_user())):
    return crud.create_notification(db, notification)

@router.get("/me", response_model=List[schemas.Notification])
def my_notifications(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Notification).filter(models.Notification.user_id == current_user.id).all()
