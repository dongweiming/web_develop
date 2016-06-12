# coding=utf-8
from flask import Flask
from werkzeug.contrib.profiler import ProfilerMiddleware

app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app)


@app.route('/')
def hello():
    return 'Hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
