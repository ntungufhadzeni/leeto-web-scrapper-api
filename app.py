from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/notice/", response_model=list[schemas.Notice])
def read_notice(db: Session = Depends(get_db)):
    notice = crud.get_notice(db)
    return notice

