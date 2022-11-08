from sqlalchemy.orm import Session
from models import Notice

def get_notice(db: Session):
    return db.query(Notice).all()