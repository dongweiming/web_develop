# coding=utf-8
from flask import Flask, request, abort
from flask_restful2 import Resource, Api

from app import db, PasteFile, humanize_bytes

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
db.init_app(app)

db.create_all(app=app)


def get_resource(paste_file):
    data = {
        'url_i': paste_file.url_i,
        'filename': paste_file.filename,
        'size': humanize_bytes(paste_file.size),
        'time': str(paste_file.uploadtime),
    }
    return data


class UploadFile(Resource):
    def get(self, file_id=0):
        if file_id != 0:
            paste_file = PasteFile.query.get_or_404(file_id)
            return {'rs': get_resource(paste_file)}
        perpage = request.args.get('perpage', 2, type=int)
        page = request.args.get('page', 1, type=int)
        rs = PasteFile.query.order_by(PasteFile.uploadtime).offset(
            (page - 1) * perpage).limit(perpage)
        return {'rs': [get_resource(pf) for pf in rs],
                'page': page, 'total': PasteFile.query.count(),
                'perpage': perpage}

    def put(self):
        uploaded_file = request.files['file']
        if not uploaded_file:
            return abort(400)
        paste_file, is_new = PasteFile.create_by_upload_file(uploaded_file)
        status_code = 201 if is_new else 200

        db.session.add(paste_file)
        db.session.commit()

        return {
            'rs': get_resource(paste_file),
            'location': paste_file.url_i
        }, status_code

    def delete(self, file_id=0):
        if file_id == 0:
            return 'The server only support delete one file', 404
        paste_file = PasteFile.query.filter(PasteFile.id == file_id).first()
        db.session.delete(paste_file)
        db.session.commit()
        return True, 204

api.add_resource(UploadFile, '/files/', endpoint='index')
api.add_resource(UploadFile, '/files/<int:file_id>/', endpoint='files')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
