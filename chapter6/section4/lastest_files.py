# coding=utf-8
import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://web:web@localhost:3306/r'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
MAX_FILE_COUNT = 50


class PasteFile(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5000), nullable=False)
    uploadtime = db.Column(db.DateTime, nullable=False)

    def __init__(self, name='', uploadtime=None):
        self.uploadtime = datetime.now() if uploadtime is None else uploadtime
        self.name = name

db.create_all()


@app.route('/upload', methods=['POST'])
def upload():
    name = request.form.get('name')

    pastefile = PasteFile(name)
    db.session.add(pastefile)
    db.session.commit()
    r.lpush('latest.files', pastefile.id)
    r.ltrim('latest.files', 0, MAX_FILE_COUNT - 1)

    return jsonify({'r': 0})


@app.route('/lastest_files')
def get_lastest_files():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=20, type=int)
    ids = r.lrange('latest.files', start, start + limit - 1)
    files = PasteFile.query.filter(PasteFile.id.in_(ids)).all()
    return json.dumps([{'id': f.id, 'filename': f.name} for f in files])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
