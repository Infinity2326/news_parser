from flask import Flask, render_template, request, url_for
import datetime
from main import create_posts
from database import connection
from gtts import gTTS


app = Flask(__name__)
create_posts()
cursor = connection.cursor()
cursor.execute("SELECT * FROM posts;")
posts = cursor.fetchall()
cursor.execute("SELECT * FROM rating;")
rating = cursor.fetchall()


@app.route('/story-<int:storyid>')
def story(storyid):
    cursor = connection.cursor()
    storyid_list = [0]
    title = [0]
    story = [0]
    for line in posts:
        storyid_list.append(line[0])
        title.append(line[1])
        story.append(line[2])

    cursor.execute("SELECT * FROM comments;")
    comments = cursor.fetchall()
    cursor.close()
    return render_template('story.html', comm=comments, postid=storyid, storyid=storyid_list[storyid], title=title[storyid], story=story[storyid])


@app.route('/story-<int:storyid>', methods=['POST', 'GET'])
def hook_comment(storyid):
    storyid_list = [0]
    title = [0]
    story = [0]
    for line in posts:
        storyid_list.append(line[0])
        title.append(line[1])
        story.append(line[2])

    if request.method == 'POST':
        cursor = connection.cursor()
        text = request.form['commentForm'].replace('"', '\"').replace("'", "\'")
        author = request.form['authorForm'].replace('"', '\"').replace("'", "\'")
        dt = datetime.datetime.now()
        dt_string = dt.strftime("Posted: %d.%m.%Y  %H:%M:%S")
        cursor.execute("INSERT INTO comments VALUES (?, ?, ?, ?)", (storyid, author, text, dt_string))
        connection.commit()
        cursor.execute("SELECT * FROM comments")
        comments = cursor.fetchall()
        cursor.close()
        return render_template('story.html', comm=comments, postid=storyid, storyid=storyid_list[storyid],
                               title=title[storyid], story=story[storyid])



@app.route('/listen-story-<int:storyid>', methods=['POST', 'GET'])
def listen_story(storyid):
    storyid_list = [0]
    title = [0]
    story = [0]
    for line in posts:
        storyid_list.append(line[0])
        title.append(line[1])
        story.append(line[2])

    text = f"{title[storyid]}  {story[storyid]}"
    language = 'en'
    tts = gTTS(text=text, lang=language, slow=False)
    ttsPath = "static/audio/music.mp3"
    tts.save(ttsPath)
    return render_template('listen.html', postid=storyid, storyid=storyid_list[storyid], title=title[storyid], story=story[storyid])


@app.route('/')
def index():
    return render_template('index.html', posts=posts, rating=rating)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
