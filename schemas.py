from pydantic import BaseModel

class NoticeBase(BaseModel):
    date : str
    title: str
    link: str


class Notice(NoticeBase):
    id: int

    class Config:
        orm_mode = True