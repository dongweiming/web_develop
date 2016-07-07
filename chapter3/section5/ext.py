# coding=utf-8
from flask_mako import MakoTemplates, render_template  # noqa
from flask_sqlalchemy import SQLAlchemy

mako = MakoTemplates()
db = SQLAlchemy()
