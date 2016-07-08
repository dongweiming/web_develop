#!/usr/bin/env python
# coding=utf-8

import os
import sys
import atexit
import code

from IPython.terminal.prompts import Prompts, Token

try:
    import IPython  # noqa
    has_ipython = True
except ImportError:
    has_ipython = False


class MyPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):   # default
        return [
            (Token.Prompt, 'In <'),
            (Token.PromptNum, str(self.shell.execution_count)),
            (Token.Prompt, '>: '),
        ]

    def out_prompt_tokens(self):
        return [
            (Token.OutPrompt, 'Out<'),
            (Token.OutPromptNum, str(self.shell.execution_count)),
            (Token.OutPrompt, '>: '),
        ]


def hook_readline_hist():
    try:
        import readline
    except ImportError:
        return

    histfile = os.environ['HOME'] + '/.web_develop_history'  # 定义一个存储历史记录的文件地址
    readline.parse_and_bind('tab: complete')
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass  # It doesn't exist yet.

    def savehist():
        try:
            readline.write_history_file(histfile)
        except:
            print 'Unable to save Python command history'
    atexit.register(savehist)


def get_banner():
    from app import app
    color_tmpl = '\x1b[{}m{}\x1b[0m'
    return color_tmpl.format(
        *(32, 'Development shell, do whatever you want.')
        if app.debug else (
            35, 'Production shell, use it carefully!'))


def pre_imports():
    from app import app, db, PasteFile  # noqa

    return locals()


def plain_shell(user_ns):
    sys.exit(code.interact(banner=get_banner(), local=user_ns))


def ipython_shell(user_ns):
    from IPython.terminal.ipapp import TerminalIPythonApp
    from IPython.terminal.interactiveshell import TerminalInteractiveShell

    class MyIPythonApp(TerminalIPythonApp):

        def init_shell(self):
            self.shell = TerminalInteractiveShell(
                prompts_class=MyPrompt, highlighting_style='emacs',
                display_banner=False, profile_dir=self.profile_dir,
                ipython_dir=self.ipython_dir, banner1=get_banner(), banner2='')
            self.shell.configurables.append(self)

    app = MyIPythonApp.instance()
    app.initialize()
    app.shell.user_ns.update(user_ns)
    sys.exit(app.start())


def main():
    hook_readline_hist()

    user_ns = pre_imports()
    use_plain_shell = not has_ipython or '--plain' in sys.argv[1:]

    if use_plain_shell:
        plain_shell(user_ns)
    else:
        ipython_shell(user_ns)


if __name__ == '__main__':
    main()
