from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    name = 'index'
    return render_template('index.html', title='This is the index page', name=name)


if __name__ == '__main__':
    app.run(debug=True)
