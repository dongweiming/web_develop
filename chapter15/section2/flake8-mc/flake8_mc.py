# coding=utf-8
import ast
from functools import partial


def msg(lineno, offset, self, msg):
    return (lineno, offset, msg, self)


USE_CLEAR_METHOD_LIST = []
NEED_CLEAR_LIST = []
IGNORE_LIST = []
MSG_MAP = {}


def main(tree, self):
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.ClassDef):
            continue

        has_clear_method = False

        for body_item in stmt.body:
            if not isinstance(body_item, ast.FunctionDef):
                continue
            item_name = body_item.name

            msg_p = partial(msg, body_item.lineno, body_item.col_offset, self)

            for item in body_item.body:
                if isinstance(item, ast.Assign):
                    value = item.value
                    if isinstance(value, ast.Str):
                        value = item.value

                        if 'select' in value.s:
                            for deco in body_item.decorator_list:
                                if isinstance(deco, ast.Call):
                                    if deco.func.id == 'cache':
                                        break
                            else:
                                yield msg_p('D012 Need `cache` decorator!')
                        elif any(op in value.s for op in ('delete', 'update')):
                            NEED_CLEAR_LIST.append(item_name)
                            MSG_MAP[item_name] = msg_p
                elif isinstance(item, ast.Expr):
                    if isinstance(item.value, ast.Call):
                        func = item.value.func
                        if isinstance(func, ast.Attribute):
                            if func.attr == 'clear_mc':
                                USE_CLEAR_METHOD_LIST.append(item_name)
                        else:
                            if func.id != 'mc_delete':
                                continue
                            for arg in item.value.args:
                                if not isinstance(arg, ast.BinOp):
                                    continue
                                if 'MC_KEY' in arg.left.attr:
                                    if body_item.name == 'clear_mc':
                                        has_clear_method = True
                elif isinstance(item, ast.If):
                    for if_item in item.body:
                        if isinstance(if_item.value, ast.Call):
                            func = if_item.value.func
                            if isinstance(func, ast.Name):
                                if func.id != 'mc_delete':
                                    continue
                                for arg in if_item.value.args:
                                    if not isinstance(arg, ast.BinOp):
                                        continue
                                    if 'MC_KEY' in arg.left.attr:
                                        IGNORE_LIST.append(item_name)

        for method_name in NEED_CLEAR_LIST:
            if method_name not in IGNORE_LIST:
                if not (has_clear_method and method_name in
                        USE_CLEAR_METHOD_LIST):
                    yield MSG_MAP[method_name]('D013 Need clear mc!')


class McChecker(object):
    name = 'flake8-mc'
    version = '0.1.0'

    def __init__(self, tree, filename):
        self.tree = tree

    def run(self):
        return main(self.tree, self)
