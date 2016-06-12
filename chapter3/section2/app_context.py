# coding=utf-8
import sqlite3

from flask import Flask, g

app = Flask(__name__)
DTABASE_FILE = 'test.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DTABASE_FILE)
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    print 'db: {}'.format(db)
    if db is not None:
        db.close()
    print 'closed'


@app.route('/')
def index():
    get_db()
    return 'Index page'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
