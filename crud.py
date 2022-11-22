from sqlalchemy.orm import Session
from models import Notice


def get_notice(db: Session):
    return db.query(Notice).all()


def get_notice_by_id(db: Session, notice_id: int):
    return db.query(Notice).filter(Notice.id == notice_id).first()
