# coding=utf-8
from flask import Flask
from plim import preprocessor
from flask_mako import MakoTemplates, render_template

mako = MakoTemplates()
app = Flask(__name__, template_folder='../../templates')
app.config['MAKO_DEFAULT_FILTERS'] = ['unicode', 'decode.utf_8', 'h']
app.config['MAKO_PREPROCESSOR'] = preprocessor
mako.init_app(app)


@app.route('/')
def index():
    return render_template('chapter3/section5/hello.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
