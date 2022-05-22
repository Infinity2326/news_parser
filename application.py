from cmath import log
import datetime
import os
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from gtts import gTTS
from posts import create_posts
from database import connection
from userlogin import UserLogin

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'loginMenu'
login_manager.login_message = "Login to see this page"
login_manager.login_message_category = "error"

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
    if not user_id:
        flask_login.logout_user()

    return UserLogin().from_database(user_id)


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
            if not current_user.is_authenticated:
                flash('Login to do this', 'error')
                return redirect(url_for('loginMenu'))

            if current_user.is_authenticated():
                user = current_user.get_id()
            else:
                return redirect(url_for('loginMenu'))

            cursor = connection.cursor()
            text = request.form['commentForm'].replace('"', '\"').replace("'", "\'")
            dt = datetime.datetime.now()
            dt_string = dt.strftime("Posted: %d.%m.%Y  %H:%M:%S")
            cursor.execute("INSERT INTO comments VALUES (?, ?, ?, ?)", (storyid, user, text, dt_string))
            connection.commit()
            cursor.execute("SELECT * FROM comments")
            comments = cursor.fetchall()
            cursor.close()
            flash('See your comment below!', 'success')
            return render_template('story.html', comm=comments, postid=storyid, storyid=storyid_list[storyid],
                                   title=title[storyid], story=story[storyid], theme=theme, user=user)


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


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        create_posts()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM posts;")
        posts = cursor.fetchall()
        cursor.execute("SELECT * FROM rating;")
        newRating = cursor.fetchall()
        cursor.close()
        return render_template('index.html', posts=posts, rating=newRating, theme=theme)


@app.route('/', methods=['POST'])
def change_rating():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM rating;")
            newRating = cursor.fetchall()
            cursor.close()
            return render_template('index.html', posts=posts, rating=newRating, theme=theme)

        elif "minus-rating" or "plus-rating" in request.form:
            cursor = connection.cursor()
            postId = request.form.get('post-id')
            postId = int(postId)
            if not current_user.is_authenticated:
                flash('Login to do this', 'error')
                return redirect(url_for('loginMenu'))

            if current_user.is_authenticated():
                user = current_user.get_id()
                newUser = user + str(postId)

            else:
                flash('Login to do this', 'error')
                return redirect(url_for('loginMenu'))

            cursor.execute(f'SELECT score FROM rating WHERE id = {postId}')
            ratingScore = cursor.fetchone()
            new = ratingScore[0]

            cursor.execute(f"SELECT user FROM ratingusers WHERE user = '{newUser}'")
            if cursor.fetchone() is not None:
                cursor.execute(f"SELECT vote FROM ratingusers WHERE user = '{newUser}'")
                vote = cursor.fetchone()
                vote = vote[0]
                if "minus-rating" in request.form:
                    if vote == "positive":
                        ratingScore = new - 2
                        newVote = "negative"
                        cursor.execute("UPDATE rating SET score = ? WHERE id = ?", (int(ratingScore), int(postId)))
                        cursor.execute("UPDATE ratingusers SET vote = ? WHERE user = ?", (newVote, newUser))
                        connection.commit()

                    elif vote == "negative":
                        flash('Already rated', 'error')
                        return redirect(url_for('index'))

                elif "plus-rating" in request.form:
                    if vote == "positive":
                        flash('Already rated', 'error')
                        return redirect(url_for('index'))

                    elif vote == "negative":
                        ratingScore = new + 2
                        newVote = "positive"
                        cursor.execute("UPDATE rating SET score = ? WHERE id = ?", (int(ratingScore), int(postId)))
                        cursor.execute("UPDATE ratingusers SET vote = ? WHERE user = ?", (newVote, newUser))
                        connection.commit()
            else:
                if "minus-rating" in request.form:
                    ratingScore = new - 1
                    newVote = "negative"
                    cursor.execute("UPDATE rating SET score = ? WHERE id = ?", (int(ratingScore), int(postId)))
                    cursor.execute("INSERT INTO ratingusers VALUES (?, ?)", (newVote, newUser))
                    connection.commit()
                else:
                    ratingScore = new + 1
                    newVote = "positive"
                    cursor.execute("UPDATE rating SET score = ? WHERE id = ?", (int(ratingScore), int(postId)))
                    cursor.execute("INSERT INTO ratingusers VALUES (?, ?)", (newVote, newUser))
                    connection.commit()

            cursor.execute("SELECT * FROM rating;")
            newRating = cursor.fetchall()
            cursor.close()
            flash('You rated this story!', 'success')
            return render_template('index.html', posts=posts, rating=newRating, theme=theme)

    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rating;")
        newRating = cursor.fetchall()
        cursor.close()
        return render_template('index.html', posts=posts, rating=newRating, theme=theme)


@app.route('/login-menu', methods=['POST', 'GET'])
def loginMenu():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('login-menu.html', theme=theme)

    if request.method == 'GET':
        return render_template('login-menu.html', theme=theme)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
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
            try:
                loginFromDB = loginFromDB[0]
            except:
                pass

            if loginFromDB == login:
                cursor.execute(f'SELECT password FROM users WHERE login="{login}"')
                hashedPassword = cursor.fetchone()
                hashedPassword = hashedPassword[0]

                if check_password_hash(hashedPassword, password):
                    userlogin = UserLogin().create_user(login)
                    login_user(userlogin)
                    flash('Successful login', 'success')
                    return redirect(url_for("profile"))

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
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
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


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if current_user.is_authenticated():
        user = current_user.get_id()
    else:
        user = None

    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return render_template('profile.html', theme=theme, user=user)

    if request.method == 'GET':
        return render_template('profile.html', theme=theme, user=user)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == 'POST':
        if "change-theme" in request.form:
            changeTheme()
            return redirect(url_for('index'))

    if request.method == 'GET':
        logout_user()
        flash('Successful logout', 'success')
        return redirect(url_for('index'))


@app.errorhandler(500)
@app.errorhandler(404)
def error_page():
    flash('Page not found', 'error')
    return redirect(url_for('index'))
