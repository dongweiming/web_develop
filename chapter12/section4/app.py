# coding=utf-8
import os
import uuid
import magic
import random
import urllib
from functools import partial
from datetime import datetime
from string import digits, ascii_uppercase, ascii_lowercase

import cropresize2
from werkzeug import SharedDataMiddleware
from flask import abort, Flask, request, jsonify, redirect, send_file
from flask_mako import MakoTemplates, render_template
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

from mimes import IMAGE_MIMES, AUDIO_MIMES, VIDEO_MIMES
from utils import get_file_md5

RANDOM_SEQ = ascii_uppercase + ascii_lowercase + digits
ONE_MONTH = 60 * 60 * 24 * 30
HERE = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='../../templates/r',
            static_folder='../../static')
app.config.from_object('config')

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/i/': os.path.join(HERE, UPLOAD_FOLDER)
})


mako = MakoTemplates(app)
db = SQLAlchemy(app)


get_file_path = partial(os.path.join, HERE, UPLOAD_FOLDER)


class PasteFile(db.Model):
    __tablename__ = 'PasteFile'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(5000), nullable=False)
    filehash = db.Column(db.String(128), nullable=False, unique=True)
    filemd5 = db.Column(db.String(128), nullable=False, unique=True)
    uploadtime = db.Column(db.DateTime, nullable=False)
    mimetype = db.Column(db.String(256), nullable=False)
    symlink = db.Column(
        db.String(50, collation='utf8_bin'), nullable=False, unique=True)
    size = db.Column(db.Integer, nullable=False)

    def __init__(self, filename='', mimetype='application/octet-stream',
                 size=0, filehash=None, symlink=None, filemd5=None):
        self.uploadtime = datetime.now()
        self.mimetype = mimetype
        self.size = int(size)
        self.filehash = filehash if filehash else self._hash_filename(filename)
        self.filename = filename if filename else self.filehash
        self.symlink = symlink if symlink else self._gen_symlink()
        self.filemd5 = filemd5

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '%s.%s' % (uuid.uuid4().hex, suffix)

    @staticmethod
    def _gen_symlink():
        return ''.join(random.sample(RANDOM_SEQ, 6))

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        return cls.query.filter_by(filehash=filehash).first() or abort(code)

    @classmethod
    def get_by_symlink(cls, symlink, code=404):
        return cls.query.filter_by(symlink=symlink).first() or abort(code)

    @classmethod
    def get_by_md5(cls, filemd5):
        return cls.query.filter_by(filemd5=filemd5).first()

    @classmethod
    def create_by_upload_file(cls, uploaded_file):
        rst = cls(uploaded_file.filename, uploaded_file.mimetype, 0)
        uploaded_file.save(rst.path)
        with open(rst.path) as f:
            filemd5 = get_file_md5(f)
            uploaded_file = cls.get_by_md5(filemd5)
            if uploaded_file:
                os.remove(rst.path)
                return uploaded_file
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        rst.filemd5 = filemd5
        return rst

    @classmethod
    def create_file_after_crop(cls, uploaded_file, width, height):
        assert uploaded_file.is_image, TypeError('Unsupported Image Type.')

        img = cropresize2.crop_resize(
            Image.open(uploaded_file), (int(width), int(height)))
        rst = cls(uploaded_file.filename, uploaded_file.mimetype, 0)
        img.save(rst.path)

        filestat = os.stat(rst.path)
        rst.size = filestat.st_size

        return rst

    @classmethod
    def create_by_old_paste(cls, filehash, symlink):
        filepath = get_file_path(filehash)
        mimetype = magic.from_file(filepath, mime=True)
        filestat = os.stat(filepath)
        size = filestat.st_size

        rst = cls(filehash, mimetype, size, filehash=filehash, symlink=symlink)
        return rst

    @property
    def path(self):
        return get_file_path(self.filehash)

    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.filehash
        return 'http://{host}/{subtype}/{hash_or_link}'.format(
            subtype=subtype, host=request.host, hash_or_link=hash_or_link)

    @property
    def url_i(self):
        return self.get_url('i')

    @property
    def url_p(self):
        return self.get_url('p')

    @property
    def url_s(self):
        return self.get_url('s', is_symlink=True)

    @property
    def url_d(self):
        return self.get_url('d')

    @property
    def image_size(self):
        if self.is_image:
            im = Image.open(self.path)
            return im.size
        return (0, 0)

    @property
    def quoteurl(self):
        return urllib.quote(self.url_i)

    @classmethod
    def create_by_img(cls, img, filename, mimetype):
        rst = cls(filename, mimetype, 0)
        img.save(rst.path)
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        return rst

    @classmethod
    def rsize(cls, old_paste, weight, height):
        assert old_paste.is_image

        img = cropresize2.crop_resize(
            Image.open(old_paste.path), (int(weight), int(height)))

        return cls.create_by_img(img, old_paste.filename, old_paste.mimetype)

    @classmethod
    def affine(cls, old_paste, w, h, a):
        assert old_paste.is_image

        img_size = (int(w), int(h))
        img = Image.open(old_paste.path).transform(
            img_size, Image.AFFINE, a, Image.BILINEAR)

        return cls.create_by_img(img, old_paste.filename, old_paste.mimetype)

    @property
    def is_image(self):
        return self.mimetype in IMAGE_MIMES

    @property
    def is_audio(self):
        return self.mimetype in AUDIO_MIMES

    @property
    def is_video(self):
        return self.mimetype in VIDEO_MIMES

    @property
    def is_pdf(self):
        return self.mimetype == 'application/pdf'

    @property
    def size_humanize(self):
        if self.size < 1024:
            return '{0} bytes'.format(self.size)
        size = self.size / 1024.0
        if size < 1024:
            size = '%.2f' % size
            return size.rstrip('0').rstrip('.') + ' KB'
        size = size / 1024.0
        size = '%.2f' % size
        return size.rstrip('0').rstrip('.') + ' MB'

    @property
    def type(self):
        for t in ('image', 'pdf', 'video', 'audio'):
            if getattr(self, 'is_' + t):
                return t
        return 'binary'


@app.route('/r/<img_hash>')
def rsize(img_hash):
    w = request.args['w']
    h = request.args['h']

    old_paste = PasteFile.get_by_filehash(img_hash)
    new_paste = PasteFile.rsize(old_paste, w, h)

    return new_paste.url_i


@app.route('/a/<img_hash>')
def affine(img_hash):
    w = request.args['w']
    h = request.args['h']

    a = request.args['a']
    a = map(float, a.split(','))

    if len(a) != 6:
        return abort(400)

    old_paste = PasteFile.get_by_filehash(img_hash)
    new_paste = PasteFile.affine(old_paste, w, h, a)

    return new_paste.url_i


@app.route('/d/<filehash>', methods=['GET'])
def download(filehash):
    paste_file = PasteFile.get_by_filehash(filehash)

    return send_file(open(paste_file.path, 'rb'),
                     mimetype='application/octet-stream',
                     cache_timeout=ONE_MONTH,
                     as_attachment=True,
                     attachment_filename=paste_file.filename.encode('utf-8'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        w = request.form.get('w')
        h = request.form.get('h')
        if not uploaded_file:
            return abort(400)

        if w and h:
            paste_file = PasteFile.create_file_after_crop(uploaded_file, w, h)
        else:
            paste_file = PasteFile.create_by_upload_file(uploaded_file)
        db.session.add(paste_file)
        db.session.commit()

        return jsonify({
            'url_d': paste_file.url_d,
            'url_i': paste_file.url_i,
            'url_s': paste_file.url_s,
            'url_p': paste_file.url_p,
            'filename': paste_file.filename,
            'size': paste_file.size_humanize,
            'time': str(paste_file.uploadtime),
            'type': paste_file.type,
            'quoteurl': paste_file.quoteurl
        })
    return render_template('index.html', **locals())


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/j', methods=['POST'])
def j():
    uploaded_file = request.files['file']

    if uploaded_file:
        paste_file = PasteFile.create_by_upload_file(uploaded_file)
        db.session.add(paste_file)
        db.session.commit()
        width, height = paste_file.image_size

        return jsonify({
            'url': paste_file.url_i,
            'short_url': paste_file.url_s,
            'origin_filename': paste_file.filename,
            'hash': paste_file.filehash,
            'width': width,
            'height': height
        })

    return abort(400)


@app.route('/p/<filehash>')
def preview(filehash):
    paste_file = PasteFile.get_by_filehash(filehash)

    filepath = get_file_path(filehash)
    if not paste_file:
        if not(os.path.exists(filepath) and (not os.path.islink(filepath))):
            return abort(404)

        linkfile = get_file_path(filehash.replace('.', '_'))
        symlink = None
        if os.path.exists(linkfile):
            with open(linkfile) as fp:
                symlink = fp.read().strip()

        paste_file = PasteFile.create_by_old_paste(filehash, symlink)
        db.session.add(paste_file)
        db.session.commit()

    return render_template('success.html', p=paste_file)


@app.route('/s/<symlink>')
def s(symlink):
    paste_file = PasteFile.get_by_symlink(symlink)

    return redirect(paste_file.url_p)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
