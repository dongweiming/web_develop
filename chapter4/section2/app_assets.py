# coding=utf-8
from flask import Flask, render_template

import assets


app = Flask(__name__)
assets.init_app(app)


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=app.debug)
