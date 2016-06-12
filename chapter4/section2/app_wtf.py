# coding=utf-8
from flask import Flask, render_template, request
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import TextField, PasswordField
from wtforms.validators import length, Required, EqualTo

from ext import db
from users import User

app = Flask(__name__, template_folder='../../templates')
app.config.from_object('config')
CsrfProtect(app)
db.init_app(app)


class RegistrationForm(Form):
    name = TextField('Username', [length(min=4, max=25)])
    email = TextField('Email Address', [length(min=6, max=35)])
    password = PasswordField('New Password', [
        Required(), EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return 'register successed!'
    return render_template('chapter4/section2/register.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=app.debug)
