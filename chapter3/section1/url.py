# coding=utf-8
from flask import Flask, url_for
app = Flask(__name__)


@app.route('/item/1/')
def item(id):
    pass


with app.test_request_context():
    print url_for('item', id='1')
    print url_for('item', id=2, next='/')
