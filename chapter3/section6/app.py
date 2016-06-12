# coding=utf-8
import MySQLdb
from werkzeug.local import LocalProxy
from flask import Flask, jsonify

from consts import HOSTNAME, DATABASE, USERNAME, PASSWORD

app = Flask(__name__)


def get_db():
    return MySQLdb.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE)


db = LocalProxy(get_db)


@app.teardown_appcontext
def close_db(error):
    db.close()


@app.route('/version')
def version():
    with db as cursor:
        cursor.execute('SELECT VERSION()')
        ver = cursor.fetchone()
    return jsonify({'version': ver[0]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
