import requests
from bs4 import BeautifulSoup


def create_story():
    stories_list = []
    for story in stories:
        stories_list.append(story.text)
    return stories_list


def create_title():
    titles_list = []
    for title in titles:
        titles_list.append(title.text)
    return titles_list


url = 'https://slashdot.org/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
stories = soup.find_all('div', class_='p')
titles = soup.find_all('span', class_='story-title')
s = create_story()
t = create_title()
