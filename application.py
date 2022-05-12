import datetime
from flask import Flask, render_template, request, url_for
from gtts import gTTS
from posts import create_posts
from database import connection
from flask_login import LoginManager


app = Flask(__name__)
theme = 'css/light-theme.css'
create_posts()
cursor = connection.cursor()
cursor.execute("SELECT * FROM posts;")
posts = cursor.fetchall()
cursor.execute("SELECT * FROM rating;")
rating = cursor.fetchall()


def changeTheme():
    global theme
    if theme == 'css/light-theme.css':
        theme = 'css/dark-theme.css'
    else:
        theme = 'css/light-theme.css'
    return theme


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
    return render_template('story.html', comm=comments, postid=storyid, storyid=storyid_list[storyid],
                           title=title[storyid], story=story[storyid], theme=theme)


@app.route('/story-<int:storyid>', methods=['POST'])
def hook_comment(storyid):
    storyid_list = [0]
    title = [0]
    story = [0]
    for line in posts:
        storyid_list.append(line[0])
        title.append(line[1])
        story.append(line[2])
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM comments")
            comments = cursor.fetchall()
            cursor.close()
            return render_template('story.html', comm=comments, postid=storyid, storyid=storyid_list[storyid],
                                   title=title[storyid], story=story[storyid], theme=theme)

        elif "authorForm" or "textForm" in request.form:
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
                                   title=title[storyid], story=story[storyid], theme=theme)


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
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('listen.html', postid=storyid, storyid=storyid_list[storyid],
                                   title=title[storyid], story=story[storyid], theme=theme)

    return render_template('listen.html', postid=storyid, storyid=storyid_list[storyid],
                           title=title[storyid], story=story[storyid], theme=theme)


@app.route('/', methods=['POST', 'GET'])
def rating_score():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM rating;")
            newRating = cursor.fetchall()
            cursor.close()
            return render_template('index.html', posts=posts, rating=newRating, theme=theme)

        if "plus-rating" in request.form:
            cursor = connection.cursor()
            postId = request.form.get('post-id')
            postId = int(postId)
            cursor.execute(f'SELECT score FROM rating WHERE id = {postId}')
            ratingScore = cursor.fetchone()
            new = ratingScore[0]
            ratingScore = new + 1
            cursor.execute("UPDATE rating SET score = ? WHERE id = ?", (ratingScore, postId))
            connection.commit()
            cursor.execute("SELECT * FROM rating;")
            newRating = cursor.fetchall()
            cursor.close()
            return render_template('index.html', posts=posts, rating=newRating, theme=theme)

        elif "minus-rating" in request.form:
            cursor = connection.cursor()
            postId = request.form.get('post-id')
            postId = int(postId)
            cursor.execute(f'SELECT score FROM rating WHERE id = {postId}')
            ratingScore = cursor.fetchone()
            new = ratingScore[0]
            ratingScore = new - 1
            cursor.execute("UPDATE rating SET score = ? WHERE id = ?", (ratingScore, postId))
            connection.commit()
            cursor.execute("SELECT * FROM rating;")
            newRating = cursor.fetchall()
            cursor.close()
            return render_template('index.html', posts=posts, rating=newRating, theme=theme)

    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rating;")
        newRating = cursor.fetchall()
        cursor.close()
        return render_template('index.html', posts=posts, rating=newRating, theme=theme)


@app.route('/login-menu', methods=['POST', 'GET'])
def loginMenu():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('login-menu.html', theme=theme)

    if request.method == 'GET':
        return render_template('login-menu.html', theme=theme)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('login.html', theme=theme)

    if request.method == 'GET':
        return render_template('login.html', theme=theme)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('registration.html', theme=theme)

        elif "registration-login" or "registration-password" in request.form:
            cursor = connection.cursor()
            newLogin = request.form['registration-login']
            newPassword = request.form['registration-password']
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            print(users)
            if not newLogin:
                return "username already taken"

            else:
                cursor.execute("INSERT INTO users VALUES (?, ?)", (newLogin, newPassword))
                connection.commit()
                cursor.close()
                return f"You registered as {newLogin} password is {newPassword}"

    if request.method == 'GET':
        return render_template('registration.html', theme=theme)
