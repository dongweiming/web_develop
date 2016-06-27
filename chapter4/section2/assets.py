# coding=utf-8
from webassets.filter import get_filter
from flask_assets import Environment, Bundle


css_common = Bundle('scss/common.scss',
                    filters='pyscss', output='css/common.css',
                    debug=False)

css_all = Bundle('css/base-min.css', css_common,
                 'css/buttons-min.css',
                 filters='cssmin', output='css/all.min.css')

js_common = Bundle('js/src/*.js', output='js/common.js')

es2015 = get_filter('babel', presets='es2015')
es2015_all = Bundle('js/src/*.es6', output='js/es6.js', filters=es2015)

js_all = Bundle(
    'js/vendor/jquery.min.js',
    js_common, es2015_all,
    filters='jsmin', output='js/all.min.js')


def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_all', js_all)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
