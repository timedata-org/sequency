import ast, functools
from . import operators, units
from . value import Value



class ExpressionBuilder(object):

    def __init__(self, import_symbol=importer.import_symbol):
        # Decorate a handler that wraps a standard operator.
        def operator(f):
            def handler(node):
                args = [self.parse(d) for d in f(node)]
                operator = operators.get(node.op)
                def function():
                    return operator(*(d() for d in args))
                return Value(function, *args)
            return handler

        def Attribute(node):  # a.b.c
            names = []
            while isinstance(node, ast.Attribute):
                names.append(node.attr)
                node = func.value
            assert isinstance(node, ast.Name)
            names.append(node.id)
            symbol = '.'.join(reversed(names))
            return Value(import_symbol(symbol))

        @operator
        def BinOp(node):  # a + b
            return node.left, node.right

        @operator
        def BoolOp(node):  # x and y and z
            return node.values

        def Call(node):  # f(a, *b, **c)
            arg = [self.parse(a) for a in node.arg]
            kwds = {k.arg: self.parse(k.value) for k in node.keywords}

            function = self.parse(node.func)
            assert isinstance(node.func, (ast.Attribute, ast.Name))
            assert function.constant

            f = functools.partial(function(), *arg, **kwds)
            return Value(f, *arg, *kwds.values())

        def Compare(node):  # 1 < 2 < 4 > 5
            left = self.parse(node.left)
            ops = [operators.get(o) for o in node.ops]
            values = [self.parse(c) for c in node.comparators]
            op_values = zip(ops, values)

            def function():
                previous = left()
                for op, value in op_values:
                    value = value()
                    if not op(previous, value):
                        return False
                    previous = value
                return True

            return Value(function, left, *values)

        def IfExp(node):  # x if y else z
            body = self.parse(node.body)
            test = self.parse(node.test)
            orelse = self.parse(node.orelse)
            function = lambda: body() if test() else orelse()
            return Value(function, body, test, orelse)

        def Name(node):
            return Value(import_symbol(node.id))

        def NameConstant(node):
            return Value(node.value)

        def Num(node):
            return Value(node.n)

        def Str(node):
            return Value(units.parse(node.s))

        @operator
        def UnaryOp(node):  # -a, not a, +a, ~a
            return node.operand,

        self.handlers = {
            ast.Attribute: Attribute,
            ast.BinOp: BinOp,
            ast.BoolOp: BoolOp,
            ast.Call: Call,
            ast.Compare: Compare,
            ast.IfExp: IfExp,
            ast.Name: Name,
            ast.NameConstant: NameConstant,
            ast.Num: Num,
            ast.Str: Str,
            ast.UnaryOp: UnaryOp,
        }

    def parse(self, node):
        return self.handlers[type(node)](node)
