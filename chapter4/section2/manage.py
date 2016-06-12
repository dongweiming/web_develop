# coding=utf-8
from flask_script import Manager, Server, Shell, prompt_bool

from app import app, db, PasteFile

manager = Manager(app)


def make_shell_context():
    return {
        'db': db,
        'PasteFile': PasteFile,
        'app': app
    }


@manager.command
def dropdb():
    if prompt_bool(
            'Are you sure you want to lose all your data'):
        db.drop_all()


@manager.option('-h', '--filehash', dest='filehash')
def get_file(filehash):
    paste_file = PasteFile.query.filter_by(filehash=filehash).first()
    if not paste_file:
        print 'Not exists'
    else:
        print 'URL is {}'.format(paste_file.get_url('i'))


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(
    use_debugger=True, use_reloader=True,
    host='0.0.0.0', port=9000)
)


if __name__ == '__main__':
    manager.run()
