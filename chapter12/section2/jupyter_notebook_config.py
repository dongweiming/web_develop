# coding=utf-8
import os
import sys

from jupyter_core.paths import jupyter_config_dir, jupyter_data_dir

sys.path.append(os.path.join(jupyter_data_dir(), 'extensions'))

c = get_config()

c.NotebookApp.open_browser = False
c.NotebookApp.password = 'sha1:19c53926b1d7:6248a00119f231540f9ba294e2739858da82bba3'
c.NotebookApp.port = 5000
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.certfile = '/home/vagrant/web_develop/chapter12/section2/mycert.pem'
c.NotebookApp.keyfile = '/home/vagrant/web_develop/chapter12/section2/mykey.key'

c.NotebookApp.extra_template_paths = [
    os.path.join(jupyter_data_dir(), 'templates')]
c.NotebookApp.server_extensions = ['nbextensions']
