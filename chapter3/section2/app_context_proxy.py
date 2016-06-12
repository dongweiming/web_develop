# coding=utf-8
import sqlite3

from flask import Flask
from werkzeug.local import LocalProxy

app = Flask(__name__)
DTABASE_FILE = 'test.db'


def get_db():
    return sqlite3.connect(DTABASE_FILE)


db = LocalProxy(get_db)


@app.teardown_appcontext
def teardown_db(exception):
    db.close()
    print 'closed'


@app.route('/')
def index():
    print db
    return 'Index page'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
