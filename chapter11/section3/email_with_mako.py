# coding=utf-8
import os
import csv
import smtplib
from email.header import Header as _Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr

from mako.template import Template
from mako.lookup import TemplateLookup

HERE = os.path.abspath(os.path.dirname(__file__))
SMTP_SERVER = 'smtp.qq.com'
# 使用标准的25端口连接SMTP服务器是明文传输，发送过程中可能会被窃听。
# 这里选择加密SMTP会话， 更安全地发送邮件
SMTP_PORT = 587
FROM_ADDR = '61966225@qq.com'
PASSWORD = 'qfqoywyxqghpbgjb'
TO_ADDRS = ['ciici123@gmail.com']

rows_data = [
    [34, 72, 38, 30, 75, 48, 75],
    [6, 24, 1, 84, 54, 62, 60],
    [28, 79, 97, 13, 85, 93, 93],
    [27, 71, 40, 17, 18, 79, 90],
    [88, 25, 33, 23, 67, 1, 59],
    [24, 100, 20, 88, 29, 33, 38],
    [6, 57, 88, 28, 10, 26, 37],
    [52, 78, 1, 96, 26, 45, 47],
    [60, 54, 81, 66, 81, 90, 80],
    [70, 5, 46, 14, 71, 19, 66],
]
col_headers = ['日期', '周一', '周二', '周三',
               '周四', '周五', '周六', '周日']
row_headers = ['用户{}'.format(i) for i in range(1, 11)]


def mako_render(data, mako_file, directories=['tmpl']):
    mylookup = TemplateLookup(directories=directories, input_encoding='utf-8',
                              output_encoding='utf-8',
                              default_filters=['decode.utf_8'])
    mytemplate = Template('<%include file="{}"/>'.format(mako_file),
                          lookup=mylookup, input_encoding='utf-8',
                          default_filters=['decode.utf_8'],
                          output_encoding='utf-8')
    content = mytemplate.render(**data)
    return content


def Header(name):  # noqa
    return _Header(name, 'utf-8').encode()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name), addr))


def gen_msg(content, subject, attachments, nick_from=None, nick_to='运营'):
    if nick_from is None:
        nick_from = FROM_ADDR
    msg = MIMEMultipart()
    msg['From'] = _format_addr('{} <{}>'.format(nick_from, FROM_ADDR))
    msg['To'] = _format_addr('{} <{}>'.format(nick_to, TO_ADDRS))
    msg['Subject'] = Header(subject)
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    for attachment in attachments:
        attach = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
        attach['Content-Type'] = 'application/octet-stream'
        attach['Content-Disposition'] = 'attachment; filename="{}"'.format(
            os.path.basename(attachment))
        msg.attach(attach)
    return msg


def sendmail(content, subject, attachments, nick_from=None):
    msg = gen_msg(content, subject, attachments, nick_from)
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(FROM_ADDR, PASSWORD)
    server.sendmail(FROM_ADDR, TO_ADDRS, msg.as_string())
    server.quit()


def write_csv(csv_file, headers, rows):
    f = open(csv_file, 'wt')
    writer = csv.writer(f)
    writer.writerow(headers)
    for index, row in enumerate(rows):
        writer.writerow([row_headers[index]] + row)
    f.close()


def main():
    csv_file = os.path.join(HERE, 'statistics.csv')
    tmpl_directories = [os.path.join(HERE, 'tmpl')]
    write_csv(csv_file, col_headers, rows_data)
    data = {'rows_data': rows_data, 'row': col_headers,
            'row_headers': row_headers}
    content = mako_render(data, 'statistics.txt', directories=tmpl_directories)
    sendmail(content, '核心用户运营数据', [csv_file], nick_from='豆瓣网')

if __name__ == '__main__':
    main()
