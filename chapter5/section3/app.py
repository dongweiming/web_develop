# coding=utf-8
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='../../templates',
            static_folder='../../static')


@app.route('/')
def index():
    return render_template('chapter5/section3/signin_fetch.html')


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    error = None
    if len(username) < 5:
        error = 'Username must be at least 5 characters'
    if len(password) < 6:
        error = 'Password must be at least 8 characters'
    elif not any(c.isupper() for c in password):
        error = 'Your password needs at least 1 capital'
    if error is not None:
        return jsonify({'r': 1, 'error': error})
    return jsonify({'r': 0, 'rs': 'Ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
