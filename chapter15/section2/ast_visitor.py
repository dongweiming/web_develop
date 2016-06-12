# coding=utf-8
import ast


class RewriteAddToSub(ast.NodeVisitor):

    def visit_Add(self, node):
        node = ast.Sub()
        return node


node = ast.parse('2 + 6', mode='eval')
node = RewriteAddToSub().visit(node)
print eval(compile(node, '<string>', 'eval'))
