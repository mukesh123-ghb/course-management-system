from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/payments", response_model=schemas.Payment)
def make_payment(
    payment: schemas.PaymentBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Process payment logic here (Stripe, PayPal, etc.)
    # Mocking success
    txn = str(uuid.uuid4())
    verified_payment = schemas.PaymentCreate(
        user_id=current_user.id,
        amount=payment.amount,
        currency=payment.currency,
        transaction_id=txn
    )
    return crud.create_payment(db, verified_payment)

@router.get("/reports/users")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    total_users = db.query(models.User).count()
    return {"total_users": total_users}

@router.get("/reports/courses")
def get_course_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    total_courses = db.query(models.Course).count()
    return {"total_courses": total_courses}
