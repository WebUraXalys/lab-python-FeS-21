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

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: schemes.UserCreate) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None 
    db_user.first_name = user_data.first_name if user_data.first_name else db_user.first_name
    db_user.second_name = user_data.second_name if user_data.second_name else db_user.second_name
    db_user.email = user_data.email if user_data.email else db_user.email


    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> None:
    db_user = db.query(models.User).get(user_id)
    if db_user:
        db.delete(db_user)
        db.commit()

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_record(db: Session, record_id: int) -> Optional[models.Record]:
    return db.query(models.Record).filter(models.Record.id == record_id).first()

def get_user_records(db: Session, user_id: int):
    return db.query(models.Record).filter(models.Record.user_id == user_id).all()

def update_record(db: Session, record_id: int, item: schemes.RecordCreate) -> Optional[models.Record]:
    db_record = db.query(models.Record).get(record_id)
    if db_record:
        db_record.title = item.title
        db_record.content = item.content
        db_record.date = item.date
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int) -> None:
    db_record = db.query(models.Record).get(record_id)
    if db_record:
        db.delete(db_record)
        db.commit()