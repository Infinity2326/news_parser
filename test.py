from flask import Flask, render_template, url_for
from main import create_posts
from database import cursor

app = Flask(__name__)


@app.route('/')
def index():
    cursor.execute("SELECT * FROM posts;")
    results = cursor.fetchall()
    return render_template('index.html', res=results)


if __name__ == "__main__":
    print('imported app')
    create_posts()
    app.run(debug=True)
