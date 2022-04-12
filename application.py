from flask import Flask, render_template, url_for
from main import create_posts
from database import cursor


app = Flask(__name__)
cursor.execute("SELECT * FROM posts;")
results = cursor.fetchall()
rating = 0

@app.route('/')
def index():
    return render_template('index.html', res=results, rating=rating)


if __name__ == "__main__":
    create_posts()
    app.run(debug=True, use_reloader=False)
