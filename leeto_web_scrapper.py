from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import datetime
from models import Notice, Base
from config import engine
import pandas as pd

url = "https://leetolapolokwane.co.za/latest-news/"

# Base.metadata.create_all(bind=engine)
Session = sessionmaker()
db = Session(bind=engine)

data = []


def scrap_website():
    html_txt = requests.get(url).text

    soup = BeautifulSoup(html_txt, 'lxml')

    posts = soup.find_all('li', class_='clr')

    for post in posts:
        row = {}
        title = post.a['title']
        link = post.a['href']
        thumbnail = post.img['src']
        date = post.find('div', class_='recent-posts-date').text.strip()[:-1]
        row['title'] = title
        row['link'] = link
        row['thumbnail'] = thumbnail
        row['date'] = date

        data.append(row)


def sort_data():
    arg_df = pd.DataFrame(data)
    arg_df['DT'] = pd.to_datetime(arg_df.date)
    arg_df.sort_values(by='DT').reset_index(inplace=True)
    return arg_df


def add_to_database(arg_df):
    for index in arg_df.index:
        date = arg_df.loc[index, 'date']
        link = arg_df.loc[index, 'link']
        title = arg_df.loc[index, 'title']
        thumbnail = arg_df.loc[index, 'thumbnail']
        try:
            new_notice = Notice(date, title, link, thumbnail)
            db.add(new_notice)
            db.commit()
        except:
            continue


if __name__ == '__main__':
    scrap_website()
    df = sort_data()
    add_to_database(df)
