from flask import Flask, render_template, url_for
from main import s, t


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', s=s, t=t)


if __name__ == "__main__":
    app.run(debug=True)
