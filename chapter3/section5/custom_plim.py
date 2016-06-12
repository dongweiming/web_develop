# coding=utf-8
import re
from plim import preprocessor_factory


PARSE_HTML_COMMENT_RE = re.compile('\/!\s+(?P<html_comment>.*)')


def parse_html_comment(indent_level, current_line, matched, source, syntax):
    html_comment = matched.group('html_comment')
    rt = '<!-- {} -->'.format(html_comment)
    return rt, indent_level, '', source


CUSTOM_PARSERS = [
    (PARSE_HTML_COMMENT_RE, parse_html_comment)
]

custom_preprocessor = preprocessor_factory(
    custom_parsers=CUSTOM_PARSERS, syntax='mako')
