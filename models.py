from sqlalchemy import Column, String, Integer, DateTime
from database import Base


class Notice(Base):
    __tablename__ = "notice"
    id = Column(Integer(), primary_key=True)
    date = Column(String(25), nullable=False)
    title = Column(String(225), nullable=False)
    link = Column(String(225), unique=True, nullable=False)

    def __init__(self, date, title, link):
        self.date = date
        self.title = title
        self.link = link