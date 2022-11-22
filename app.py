from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/notice/", response_model=list[schemas.Notice])
async def read_notice(db: Session = Depends(get_db)):
    return crud.get_notice(db)


@app.get("/api/article/{notice_id}")
async def get_article(notice_id: int, db: Session = Depends(get_db)):
    notice = crud.get_notice_by_id(db, notice_id)
    url = notice.link
    html_txt = requests.get(url).text
    soup = BeautifulSoup(html_txt, 'lxml')
    try:
        article = soup.find_all('div', class_='elementor-text-editor elementor-clearfix')[0]
    except IndexError:
        article = soup.find_all('main', class_='site-main clr')[0]

    paragraphs = str(article).split('\n')
    paragraph = ' '.join(paragraphs)

    return {'data': paragraph}
