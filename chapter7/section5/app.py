# coding=utf-8
from flask import Flask
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app, dsn='http://8bf67e879e8d48208cebd00b1994e812:0b9c297690dd477c8147ae6b19953914@localhost:5000/2')  # noqa


@app.route('/error')
def error():
    try:
        1 / 0
    except ZeroDivisionError:
        sentry.captureException()
    return 'error'


@app.route('/raise')
def auto_raise():
    raise IndexError


@app.route('/log')
def log():
    sentry.captureMessage('hello, world!')
    return 'logging'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
