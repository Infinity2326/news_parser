from flask import Flask, render_template, request, url_for
from main import create_posts
from database import cursor


app = Flask(__name__)
create_posts()
cursor.execute("SELECT * FROM posts;")
posts = cursor.fetchall()
cursor.execute("SELECT * FROM rating;")
rating = cursor.fetchall()


@app.route('/story-<int:storyid>', methods=['GET', 'POST'])
def story(storyid):
    storyid_list = [0]
    title = [0]
    story = [0]
    for line in posts:
        storyid_list.append(line[0])
        title.append(line[1])
        story.append(line[2])

    if request.method == 'POST':
        author = request.form.get("author")
        print(f"Author's name {author}")
    else:
        print('method get')

    return render_template('story.html', storyid=storyid_list[storyid], title=title[storyid], story=story[storyid])


@app.route('/')
def index():
    return render_template('index.html', posts=posts, rating=rating)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
