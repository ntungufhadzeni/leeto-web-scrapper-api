from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import datetime
from models import Notice, Base
from config import engine

url = "https://leetolapolokwane.co.za/latest-news/"

Base.metadata.create_all(bind=engine)
Session = sessionmaker()
db = Session(bind=engine)


def scrap_website():
    html_txt = requests.get(url).text

    soup = BeautifulSoup(html_txt, 'lxml')

    posts = soup.find_all('li', class_='clr')

    for post in posts:
        title = post.a['title']
        link = post.a['href']
        thumbnail = post.img['src']
        date = post.find('div', class_='recent-posts-date').text.strip()[:-1]

        try:
            new_notice = Notice(date, title, link, thumbnail)
            db.add(new_notice)
            db.commit()
        except:
            continue


if __name__ == '__main__':
    scrap_website()
