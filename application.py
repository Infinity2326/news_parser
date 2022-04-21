from flask import Flask, render_template, url_for
from main import create_posts
from database import cursor


app = Flask(__name__)
create_posts()
cursor.execute("SELECT * FROM posts;")
posts = cursor.fetchall()
cursor.execute("SELECT * FROM rating;")
rating = cursor.fetchall()


@app.route('/story-<int:storyid>')
def story(storyid):
    title = [0]
    story = [0]
    for line in posts:
        title.append(line[1])
        story.append(line[2])
    return render_template('story.html', title=title[storyid], story=story[storyid])


@app.route('/')
def index():
    return render_template('index.html', posts=posts, rating=rating)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
