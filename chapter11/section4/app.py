# coding=utf-8
import os
import cStringIO
from datetime import date, datetime

import pandas as pd
from flask import Flask, send_file, render_template

app = Flask(__name__, template_folder='../../templates',
            static_folder='../../static')
HERE = os.path.abspath(os.path.dirname(__file__))
CSV_DIRECTORY = '~/web_develop/chapter11/section4/csv'


def _get_frame(date_string):
    if date_string is None:
        date_string = date.today().strftime('%Y%M%d')
    else:
        try:
            datetime.strptime(date_string, '%Y%M%d')
        except ValueError:
            return False
    df = pd.read_csv(os.path.join(
        CSV_DIRECTORY, '{}.csv'.format(date_string)))
    return df


@app.route('/csv/<date_string>')
def show_tables(date_string=None):
    df = _get_frame(date_string)
    if isinstance(df, bool) and not df:
        return 'Bad date format!'
    return render_template(
        'chapter11/section4/csv.html', df=df.to_html(classes='frame'),
        date_string=date_string)


@app.route('/csv/download/<date_string>/<int:user_index>')
def serve_csv(date_string=None, user_index=None):
    buffer = cStringIO.StringIO()
    df = _get_frame(date_string)
    if isinstance(df, bool) and not df:
        return 'Bad date format!'
    if user_index is not None:
        df = df.loc[user_index - 1]  # 事实上返回的是一个Series
    df.to_csv(buffer, encoding='utf-8')
    buffer.seek(0)
    return send_file(
        buffer, attachment_filename='{}.csv'.format(date_string),
        as_attachment=True, mimetype='text/csv')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)
