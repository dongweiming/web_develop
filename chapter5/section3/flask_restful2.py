# coding=utf-8
import urllib
import urlparse
from json import dumps
from collections import OrderedDict

from flask import request, make_response, g
from flask.views import MethodView
from werkzeug.wrappers import Response
from werkzeug.exceptions import (
    HTTPException, PreconditionRequired, PreconditionFailed)
from werkzeug.http import generate_etag
from werkzeug.local import LocalStack, LocalProxy
from flask_restful import Api as RESTApi, unpack

LINK_TMPL = '<{link}>; rel="{rel}"'

_path_ctx_local = LocalStack()


def _find_path():
    top = _path_ctx_local.top
    if top is None:
        _path_ctx_local.push({})
        top = _path_ctx_local.top
    return top

PATH_MAP = LocalProxy(_find_path)


class NotModified(HTTPException):
    code = 304

    def get_response(self, env=None):
        return Response(status=self.code)


def handle_error(message, code=400):
    dumped = dumps({'message': message}) + '\n'
    resp = make_response(dumped, code)
    return resp


def update_url(url, params):
    '''
    >>> url = 'http://www.douban.com/?page=1'
    >>> update_url(url, {'page': 2})
    'http://www.douban.com/?page=2'
    >>> url = 'http://www.douban.com/'
    >>> update_url(url, {'page': 2})
    'http://www.douban.com/?page=2'
    '''
    if not url or not isinstance(params, dict):
        return url
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)


def handle_etag(resp):
    if not getattr(g, 'condtnl_etags_start', False):
        return
    etag = generate_etag(resp.data)
    g.condtnl_etags_start = False
    url = request.url

    if request.method == 'DELETE':
        if url in PATH_MAP:
            del PATH_MAP[request.url]
        del resp.headers['etag']
    elif (request.method == 'GET' and
          request.if_none_match and
          etag in request.if_none_match):
        raise NotModified

    resp.set_etag(etag)
    PATH_MAP[url] = etag
    resp.make_conditional(request)


def add_link_header(headers, data):
    current_page = request.args.get('page') or data.get('page')
    total = headers.get('X-Total-Count')
    if current_page is not None and total is not None:
        current_page = int(current_page)
        link = update_url(request.url, {'page': current_page})
        links = [
            LINK_TMPL.format(
                link=link, page=current_page, rel='self'),
            LINK_TMPL.format(
                link=update_url(request.url, {'page': 1}), rel='first')
        ]
        perpage = request.args.get('perpage') or data.get('perpage')
        prev_page = current_page - 1
        next_page = current_page + 1
        if total and perpage is not None:
            perpage = int(perpage)
            total = int(total)
            total_page = total / perpage + (
                1 if total % perpage else 0)
            if next_page <= total_page:
                links.extend([
                    LINK_TMPL.format(
                        link=update_url(request.url, {'page': next_page}),
                        rel='next'),
                    LINK_TMPL.format(
                        link=update_url(request.url, {'page': total_page}),
                        rel='last')
                ])
        if current_page > 1:
            links.append(
                LINK_TMPL.format(
                    link=update_url(
                        request.url, {'page': prev_page}), rel='prev')
            )
        headers['Link'] = ','.join(links)


def output_json(data, code, headers=None):
    if isinstance(data, dict) and 'message' not in data:
        for k in ('rs', 'result'):
            if k in data:
                dumped = dumps(data[k]) + '\n'
                break
        else:
            return handle_error(
                'You need use `rs` or `result` as the response key')

    else:
        dumped = dumps(data) + '\n'

    resp = make_response(dumped, code)

    if isinstance(data, dict):
        for k in ('count', 'total'):
            if k in data:
                resp.headers.add('X-Total-Count', data[k])
        for k in ('loc', 'location'):
            if k in data:
                resp.headers.add('Location', data[k])
                break
        else:
            if code == 201:
                return handle_error(
                    'You need add `loc` or `location` for response '
                    'header `Location`')
        add_link_header(resp.headers, data)
    resp.headers.extend(headers or {})
    handle_etag(resp)
    return resp

DEFAULT_REPRESENTATIONS = [('application/json', output_json)]


class Api(RESTApi):
    def __init__(self, app=None, prefix='',
                 default_mediatype='application/json', decorators=None,
                 catch_all_404s=False, serve_challenge_on_401=False,
                 url_part_order='bae', errors=None):
        super(Api, self).__init__(
            app, prefix, default_mediatype, decorators, catch_all_404s,
            serve_challenge_on_401, url_part_order, errors)
        self.representations = OrderedDict(DEFAULT_REPRESENTATIONS)


class Resource(MethodView):
    representations = None
    method_decorators = []

    def check_headers(self):
        for accept in ('*/*', 'application/json'):
            if accept in request.headers['Accept']:
                break
        else:
            return 'Accept Only support `*/*` or `application/json`'

    def check_etag(self):
        etag = PATH_MAP.get(request.url, None)
        if request.method == 'DELETE':
            if not request.if_match:
                raise PreconditionRequired
            if etag is None or etag not in request.if_match:
                raise PreconditionFailed

    def dispatch_request(self, *args, **kwargs):
        self.check_etag()
        message = self.check_headers()
        if message is not None:
            return handle_error(message)

        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        for decorator in self.method_decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        g.condtnl_etags_start = True

        if isinstance(resp, Response):
            return resp

        representations = self.representations or OrderedDict()

        mediatype = request.accept_mimetypes.best_match(
            representations, default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers['Content-Type'] = mediatype
            return resp

        return resp

if __name__ == '__main__':
    import doctest
    doctest.testmod()
