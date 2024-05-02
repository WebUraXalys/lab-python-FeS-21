from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemes, crud
from app.database import get_db

records_router = APIRouter(prefix="/records", tags=["records"])

# "http://localhost:8000/records"


@records_router.post("/", response_model=schemes.Record)
def create_record(record: schemes.RecordCreate, user_id: int, db: Session = Depends(get_db)):
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_record(db, item=record, user_id=user_id)


@records_router.get("/{record_id}", response_model=schemes.Record)
def get_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_record(db, record_id=record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record


@records_router.get("/user/{user_id}", response_model=list[schemes.Record])
def get_records_by_user(user_id: int, db: Session = Depends(get_db)):
    db_records = crud.get_user_records(db, user_id=user_id)
    if not db_records:
        raise HTTPException(status_code=404, detail="No records found for this user")
    return db_records


@records_router.put("/{record_id}", response_model=schemes.Record)
def update_record(record_id: int, record: schemes.RecordCreate, db: Session = Depends(get_db)):
    db_record = crud.update_record(db, record_id=record_id, item=record)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record


@records_router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    if not crud.get_record(db, record_id):
        raise HTTPException(status_code=404, detail="Record not found")
    crud.delete_record(db, record_id)
    return {"detail": "Record deleted"}


