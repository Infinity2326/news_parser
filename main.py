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

    for i in range(len(titles_list)):
        title = titles_list[i]
        sql_request = f'SELECT * FROM posts WHERE title="{title}";'
        sql_request = cursor.execute(sql_request).fetchone()
        if not sql_request:
            cursor.execute("INSERT INTO posts VALUES (?, ?, ?)", (None, title, stories_list[i]))
            connection.commit()
        else:
            pass



url = 'https://slashdot.org/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
stories = soup.find_all('div', class_='p')
titles = soup.find_all('span', class_='story-title')
