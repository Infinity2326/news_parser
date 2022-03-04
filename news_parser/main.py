import requests
from bs4 import BeautifulSoup


def create_story():
    stories_list = [0] * 15
    titles_list = [0] * 15
    i = 0
    j = 0
    for story in stories:
        stories_list[i] = story.text
        i += 1

    for title in titles:
        titles_list[j] = title.text
        j += 1

    with open("html/main.html", "a") as file:
        for j in range(len(stories_list)):
            new_story = f'<div class = "topic">{titles_list[j]}</div>\n<div class="story">{stories_list[j]}</div>\n'
            file.writelines(new_story)
        file.writelines('</body>\n</html>')


url = 'https://slashdot.org/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
stories = soup.find_all('div', class_='p')
titles = soup.find_all('span', class_='story-title')

create_story()
