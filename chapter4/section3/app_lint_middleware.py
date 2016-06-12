# coding=utf-8
from flask import Flask
from werkzeug.contrib.lint import LintMiddleware

app = Flask(__name__)
app.wsgi_app = LintMiddleware(app.wsgi_app)


@app.route('/')
def hello():
    return 'Hello', 10


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
