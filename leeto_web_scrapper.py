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
session = Session(bind=engine)


def scrap_website():
    html_txt = requests.get(url).text

    soup = BeautifulSoup(html_txt, 'lxml')

    posts = soup.find_all('li', class_='clr')

    for post in posts:
        title = post.a['title']
        link = post.a['href']
        thumbnail = post.img['src']
        date_str = post.find('div', class_='recent-posts-date').text.strip()[:-1]
        date = datetime.datetime.strptime(date_str, '%B %d, %Y').strftime('%B %d, %Y')
       
        try:
            new_notice = Notice(date, title, link, thumbnail)
            session.add(new_notice)
            session.commit()
        except:
            print('pass')
            continue


if __name__ == '__main__':
    scrap_website()
