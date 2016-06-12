# coding=utf-8
import sys

sys.path.append('gen-py')
sys.path.insert(0, '/usr/lib/python2.7/site-packages')

from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol

from pastefile import PasteFileService
from pastefile.ttypes import (
    PasteFile, CreatePasteFileRequest, UploadImageError,
    NotFound)

from werkzeug.local import LocalProxy


def get_client():
    transport = TSocket.TSocket('localhost', 8200)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = PasteFileService.Client(protocol)
    transport.open()
    return client

client = LocalProxy(get_client)


def create(uploaded_file, width=None, height=None):
    filename = uploaded_file.filename.encode('utf-8')
    mimetype = uploaded_file.mimetype.encode('utf-8')
    filehash, path = client.get_file_info(filename, mimetype)

    create_request = CreatePasteFileRequest()

    create_request.filename = filename
    create_request.mimetype = mimetype
    create_request.filehash = filehash

    uploaded_file.save(path)
    if width is not None and height is not None:
        create_request.width = width
        create_request.height = height
    try:
        pastefile = client.create(create_request)
    except UploadImageError:
        return {'r': 1, 'error': 'upload fail'}

    print isinstance(pastefile, PasteFile)

    try:
        paste_file = client.get(pastefile.id)
    except NotFound:
        return {'r': 1, 'error': 'not found'}

    return {'r': 0, 'paste_file': paste_file}
