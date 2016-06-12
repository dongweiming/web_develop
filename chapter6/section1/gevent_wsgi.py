# coding=utf-8
import argparse

from gevent.wsgi import WSGIServer
from app import app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='server port',
                        type=int, default=9000)
    args = parser.parse_args()
    http_server = WSGIServer(('', args.port), app)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
