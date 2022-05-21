import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, login_user, login_required
from gtts import gTTS
from posts import create_posts
from database import connection
from userlogin import UserLogin


app = Flask(__name__)
#app.config(dict(DATABASE=os.path.join(app.root_path, 'database.db')))
login_manager = LoginManager(app)

theme = 'css/light-theme.css'

cursor = connection.cursor()
cursor.execute("SELECT * FROM posts;")
posts = cursor.fetchall()
cursor.execute("SELECT * FROM rating;")
rating = cursor.fetchall()
create_posts()

def changeTheme():
    global theme
    if theme == 'css/light-theme.css':
        theme = 'css/dark-theme.css'
    else:
        theme = 'css/light-theme.css'
    return theme

@login_manager.user_loader
def load_user(user_id):
    print("LOAD USER ")
    return UserLogin.from_database(user_id)


@app.route('/story-<int:storyid>')
@login_required
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

        elif "login-login" or "login-password" in request.form:
            cursor = connection.cursor()
            login = request.form['login-login']
            password = request.form['login-password']
            cursor.execute(f'SELECT login FROM users WHERE login="{login}"')
            loginFromDB = cursor.fetchone()
            loginFromDB = loginFromDB[0]
            if loginFromDB == login:
                cursor.execute(f'SELECT password FROM users WHERE login="{login}"')
                hashedPassword = cursor.fetchone()
                hashedPassword = hashedPassword[0]
                if check_password_hash(hashedPassword, password):
                    userlogin = UserLogin().create_user(login)
                    login_user(userlogin)
                    flash('Successful login', 'success')
                    return redirect(url_for("rating_score"))
                else:
                    flash('Wrong login or password', 'error')
                    return redirect(url_for("login"))
            else:
                flash('Wrong login or password', 'error')
                return redirect(url_for("login"))

    if request.method == 'GET':
        return render_template('login.html', theme=theme)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('registration.html', theme=theme)

        elif "registration-login" or "registration-password" in request.form:
            if len(request.form['registration-login']) >= 4 and len(request.form['registration-password']) >= 6 \
            and request.form['registration-password'] == request.form['registration-password2']:
                cursor = connection.cursor()
                newLogin = request.form['registration-login']
                newPassword = request.form['registration-password']
                passwordHash = generate_password_hash(newPassword)
                cursor.execute(f'SELECT login FROM users WHERE login="{newLogin}"')
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (None, newLogin, passwordHash))
                    connection.commit()
                    cursor.close()
                    flash('Successful registration', 'success')
                    return redirect(url_for("loginMenu"))

                else:
                    flash('This name is already registered', 'error')
                    return redirect(url_for("registration"))
            else:
                flash('Passwords are different', 'error')
                return redirect(url_for("registration"))

    if request.method == 'GET':
        return render_template('registration.html', theme=theme)
