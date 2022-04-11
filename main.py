import requests
from bs4 import BeautifulSoup
from database import *


def create_posts():
    titles_list = []
    stories_list = []
    for title in titles:
        titles_list.append(title.text.replace('"', '.').replace("'", '.'))

    for story in stories:
        stories_list.append(story.text.replace('"', '.').replace("'", '.'))

    cursor.execute("SELECT * FROM posts;")
    db = cursor.fetchall()

    for i in range(len(titles_list)):
        if len(db) == 0:
            cursor.execute("INSERT INTO posts VALUES (?, ?, ?)", (None, titles_list[i], stories_list[i]))
        for one in db:
            if titles_list[i] == one[1]:
                pass

            else:
                cursor.execute("INSERT INTO posts VALUES (?, ?, ?)", (None, titles_list[i], stories_list[i]))

    cursor.execute("SELECT * FROM posts;")
    connection.commit()


url = 'https://slashdot.org/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
stories = soup.find_all('div', class_='p')
titles = soup.find_all('span', class_='story-title')
