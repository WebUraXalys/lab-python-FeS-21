from app import schemes, crud
from app.database import get_db

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

users_router = APIRouter(prefix="/users", tags=["users"])

# "http//:localhost:8000/users"


@users_router.post("/", response_model=schemes.User)
def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User with email={user.email} already exists")

    db_user = crud.create_user(db, user=user)
    return db_user

