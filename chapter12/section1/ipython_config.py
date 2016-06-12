# coding=utf-8
c = get_config()
c.TerminalIPythonApp.display_banner = False
c.InteractiveShell.automagic = True
c.AliasManager.user_aliases = [
    ('la', 'ls -al')
]
c.InteractiveShell.colors = 'Linux'
c.InteractiveShell.logstart = True
c.TerminalInteractiveShell.confirm_exit = False
c.StoreMagics.autorestore = True
