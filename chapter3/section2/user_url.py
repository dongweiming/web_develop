# coding=utf-8
import time

from flask import Flask, redirect, url_for

app = Flask(__name__)


def get_fake_user():
    return {
        'username': 'user1',
        'photos': 'photos',
        'notes': 'notes'
    }


@app.route('/user/')
def user():
    user = get_fake_user()
    return user['username']


@app.route('/user/photos/')
def user_photos():
    user = get_fake_user()
    return user['photos']


@app.route('/user/notes/')
def user_notes():
    user = get_fake_user()
    return user['notes']


@app.route('/user/<username>/redirect/')
def user_redirect(username):
    return redirect(url_for('user_photos', username=username,
                            r=int(time.time())))


@app.route('/user/<username>/redirect2/')
def user_redirect2(username):
    return redirect(url_for('user_notes', username=username,
                            r=int(time.time())))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
