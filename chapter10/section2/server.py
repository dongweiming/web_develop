# coding=utf-8
import os
import sys
from datetime import datetime

sys.path.append('gen-py')
sys.path.append('/usr/lib/python2.7/site-packages')

from flask_sqlalchemy import SQLAlchemy

from app import app
from models import PasteFile as BasePasteFile
from utils import get_file_md5

db = SQLAlchemy(app)

from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from pastefile import PasteFileService
from pastefile.ttypes import PasteFile, UploadImageError, NotFound


class RealPasteFile(db.Model, BasePasteFile):
    def __init__(self, *args, **kwargs):
        BasePasteFile.__init__(self, *args, **kwargs)

    @classmethod
    def create_by_upload_file(cls, uploaded_file):
        rst = uploaded_file
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

    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.filehash
        return 'http://%s/{subtype}/{hash_or_link}'.format(
            subtype=subtype, hash_or_link=hash_or_link)


class PasteFileHandler(object):
    def get_file_info(self, filename, mimetype):
        rst = RealPasteFile(filename, mimetype, 0)
        return rst.filehash, rst.path

    def create(self, request):
        width = request.width
        height = request.height

        upload_file = RealPasteFile(request.filename, request.mimetype, 0,
                                    request.filehash)

        try:
            if width and height:
                paste_file = RealPasteFile.rsize(upload_file, width, height)
            else:
                paste_file = RealPasteFile.create_by_upload_file(
                    upload_file)
        except:
            raise UploadImageError()
        db.session.add(paste_file)
        db.session.commit()
        return self.convert_type(paste_file)

    def get(self, pid):
        paste_file = RealPasteFile.query.filter_by(id=pid).first()
        if not paste_file:
            raise NotFound()
        return self.convert_type(paste_file)

    @classmethod
    def convert_type(cls, paste_file):
        '''将模型转化为Thrift结构体的类型'''
        new_paste_file = PasteFile()
        for attr in ('id', 'filehash', 'filename', 'filemd5', 'uploadtime',
                     'mimetype', 'symlink', 'size', 'quoteurl', 'size', 'type',
                     'url_d', 'url_i', 'url_s', 'url_p'):
            val = getattr(paste_file, attr)
            if isinstance(val, unicode):
                val = val.encode('utf-8')
            if isinstance(val, datetime):
                val = str(val)
            setattr(new_paste_file, attr, val)
        return new_paste_file


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    handler = PasteFileHandler()
    processor = PasteFileService.Processor(handler)
    transport = TSocket.TServerSocket(port=8200)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadPoolServer(
        processor, transport, tfactory, pfactory)
    print 'Starting the server...'
    server.serve()
