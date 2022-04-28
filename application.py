from flask import Flask, render_template, request, url_for
from main import create_posts
from database import cursor, connection


app = Flask(__name__)
create_posts()
cursor.execute("SELECT * FROM posts;")
posts = cursor.fetchall()
cursor.execute("SELECT * FROM rating;")
rating = cursor.fetchall()
cursor.execute("SELECT * FROM comments;")
comments = cursor.fetchall()


@app.route('/story-<int:storyid>')
def story(storyid):
    storyid_list = [0]
    title = [0]
    story = [0]
    for line in posts:
        storyid_list.append(line[0])
        title.append(line[1])
        story.append(line[2])

    return render_template('story.html', storyid=storyid_list[storyid], title=title[storyid], story=story[storyid])


@app.route('/story-<int:storyid>', methods=['POST', 'GET'])
def hook_comment(storyid):
    if request.method == 'POST':
        text = request.form['commentForm']
        author = request.form['authorForm']
        cursor.execute("INSERT INTO comments VALUES (?, ?, ?)", (None, author, text))
        connection.commit()
    return f"{author} said: {text}"


@app.route('/')
def index():
    return render_template('index.html', posts=posts, rating=rating)

# testing
# @app.route('/', methods=['POST', 'GET'])
# def check_rating():
#     if request.method == 'POST':
#         rating = request.form['rating-system']
#     else:
#         print('method get')
#
#     return rating


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
