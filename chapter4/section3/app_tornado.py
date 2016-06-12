# coding=utf-8
import logging

import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado.web import Application
from tornado.options import define, options, parse_command_line
from werkzeug.debug import DebuggedApplication
from werkzeug.debug.tbtools import get_current_traceback


class Handler(tornado.web.RequestHandler):
    def initialize(self, debug):
        if debug:
            self.write_error = self.write_debugger_error

    def write_debugger_error(self, status_code, **kwargs):
        assert isinstance(self.application, DebugApplication)
        html = self.application.render_exception()
        self.write(html.encode('utf-8', 'replace'))


class BadHandler(Handler):
    def get(self):
        raise Exception('This is a test')
        self.write('You will never see this text.')


class RequestDispatcher(tornado.web._RequestDispatcher):
    def set_request(self, request):
        super(RequestDispatcher, self).set_request(request)
        if '__debugger__' in request.uri:
            return self.application.debug_container(request)


class DebugApplication(Application):
    def __init__(self, *args, **kwargs):
        super(DebugApplication, self).__init__(*args, **kwargs)
        self.debug_app = DebuggedApplication(self, evalex=True)
        self.debug_container = tornado.wsgi.WSGIContainer(self.debug_app)

    def start_request(self, server_conn, request_conn):
        return RequestDispatcher(self, request_conn)

    def render_exception(self):
        traceback = get_current_traceback()

        for frame in traceback.frames:
            self.debug_app.frames[frame.id] = frame
        self.debug_app.tracebacks[traceback.id] = traceback

        return traceback.render_full(evalex=True,
                                     secret=self.debug_app.secret)


def create_application(debug=False):
    handlers = [
        ('/error/', BadHandler, {'debug': debug}),
    ]
    if debug:
        return DebugApplication(handlers, debug=True)
    return Application(handlers, debug=debug)


def main():
    define('debug', default=False, type=bool, help='Run in debug mode.')
    define('port', default=9000, type=int, help='Port on which to listen.')
    parse_command_line()

    logger = logging.getLogger()
    port = options.port
    application = create_application(debug=options.debug)
    logger.info('Running tornado on port {}.'.format(port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
