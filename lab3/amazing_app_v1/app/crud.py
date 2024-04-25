from typing import Union, Optional

from app import models
from app import schemes

from sqlalchemy.orm import Session

import hashlib


def create_user(db: Session, user: schemes.UserCreate) -> schemes.User:
    hashed_password = hashlib.md5(user.password.encode())
    db_user = models.User(email=user.email, first_name=user.first_name,
                          second_name=user.second_name, password=hashed_password.hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_record(db: Session, item: schemes.RecordCreate, user_id: int) -> schemes.Record:
    db_record = models.Record(**item.dict(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

