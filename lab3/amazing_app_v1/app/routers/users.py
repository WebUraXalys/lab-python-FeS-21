from app import schemes, crud
from app.database import get_db

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

users_router = APIRouter(prefix="/users", tags=["users"])




@users_router.post("/", response_model=schemes.User)
def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)) -> schemes.User:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User with email={user.email} already exists")

    db_user = crud.create_user(db, user=user)
    return db_user


@users_router.get("/by-email/", response_model=schemes.User)
def get_user_by_email(email: str = None, db: Session = Depends(get_db)):
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with email={email} does not exist")
    return db_user

@users_router.get("/{user_id}", response_model=schemes.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.put("/{user_id}", response_model=schemes.User)
def update_user(user_id: int, user_data: schemes.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_data=user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    return {"detail": "User deleted"}

@users_router.get("/", response_model=list[schemes.User])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users