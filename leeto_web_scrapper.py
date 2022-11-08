from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import datetime
from models import Notice


url = "https://leetolapolokwane.co.za/latest-news/"


DATABASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = f'sqlite:///{DATABASE_DIR}/notice.db'

Session = sessionmaker()
engine = create_engine(DATABASE_URI)
session = Session(bind=engine)


def scrap_website():
    html_txt = requests.get(url).text

    soup = BeautifulSoup(html_txt, 'lxml')

    posts = soup.find_all('div', class_='recent-posts-details-inner clr')

    for post in posts:
        title = post.a['title']
        link = post.a['href']
        date_str = post.find('div', class_='recent-posts-date').text.strip()[:-1]
        date = datetime.datetime.strptime(date_str, '%B %d, %Y').strftime('%d/%m/%Y')
       

        try:
            new_notice = Notice(date, title, link)
            session.add(new_notice)
            session.commit()
        except:
            continue


if __name__ == '__main__':
    scrap_website()
