# coding=utf-8
import time

from flask import Flask, g, url_for, redirect

app = Flask(__name__)


def get_fake_user(username):
    return {
        'username': username,
        'photos': 'photos',
        'notes': 'notes'
    }


@app.url_defaults
def add_user_url(endpoint, values):
    if not endpoint or not endpoint.startswith('user'):
        return
    if 'r' not in values:
        values['r'] = int(time.time())
    if 'username' not in values:
        values['username'] = g.user['username']


@app.url_value_preprocessor
def pull_user_url(endpoint, values):
    if not endpoint or not endpoint.startswith('user'):
        return
    username = values.get(
        'username', 'default_user') if values else 'default_user'
    g.user = get_fake_user(username)


@app.route('/user/<username>/')
def user(username):
    return g.user['username']


@app.route('/user/<username>/photos')
def user_photos(username):
    return g.user['photos']


@app.route('/user/<username>/notes')
def user_notes(username):
    return g.user['notes']


@app.route('/user/<username>/redirect/')
def user_redirect(username):
    return redirect(url_for('user_photos'))


@app.route('/user/<username>/redirect2/')
def user_redirect2(username):
    return redirect(url_for('user_notes'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
