# coding=utf-8
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

from app import app


def main():
    define('port', default=9000, type=int, help='Port on which to listen.')
    parse_command_line()

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(options.port)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
