import ast, functools
from . import operators, importer, units
from . value import Constant, Value


class ExpressionBuilder(object):

    def __init__(self, symbol_table=importer.import_symbol):

        # Decorate a handler that wraps a standard operator.
        def operator(f):
            def handler(node):
                args = [self.expression(d) for d in f(node)]
                operator = operators.get(node.op)

                def function():
                    return operator(*(d() for d in args))

                return Value(function, *args)
            return handler

        # Handle lists, tuples and sets.
        def list_maker(node, maker):
            elts = [self.expression(e) for e in node.elts]

            def function():
                return maker(e() for e in elts)

            return Value(function, *elts)

        # All these next functions are handlers, which process an ast node.
        # Their names correspond exactly to the name in the ast module,
        # so ast.Attribute, ast.BinOp and the like.

        def Attribute(node):  # a.b.c
            names = []
            while isinstance(node, ast.Attribute):
                names.append(node.attr)
                node = node.value
            assert isinstance(node, ast.Name)
            names.append(node.id)
            symbol = '.'.join(reversed(names))
            return Value(symbol_table(symbol))

        @operator
        def BinOp(node):  # a + b
            return node.left, node.right

        @operator
        def BoolOp(node):  # x and y and z
            return node.values

        def Call(node):  # f(a, *b, **c)
            arg = [self.expression(a) for a in node.arg]
            kwds = {k.arg: self.expression(k.value) for k in node.keywords}

            function = self.expression(node.func)
            assert isinstance(node.func, (ast.Attribute, ast.Name))
            assert function.constant

            f = functools.partial(function(), *arg, **kwds)
            return Value(f, *(arg + list(kwds.values())))

        def Compare(node):  # 1 < 2 < 4 > 5
            left = self.expression(node.left)
            ops = [operators.get(o) for o in node.ops]
            values = [self.expression(c) for c in node.comparators]
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

        def Expr(node):
            return self.expression(node.value)

        def IfExp(node):  # x if y else z
            body = self.expression(node.body)
            test = self.expression(node.test)
            orelse = self.expression(node.orelse)

            def function():
                return body() if test() else orelse()

            return Value(function, body, test, orelse)

        def List(node):
            return list_maker(node, list)

        def Module(node):
            return node.body and self.expression(node.body[0]) or Constant(None)

        def Name(node):
            return Value(symbol_table(node.id))

        def NameConstant(node):
            return Value(node.value)

        def Num(node):
            return Value(node.n)

        def Set(node):
            return list_maker(node, set)

        def Str(node):
            return Value(node.s)

        def Tuple(node):
            return list_maker(node, tuple)

        @operator
        def UnaryOp(node):  # -a, not a, +a, ~a
            return node.operand,

        # Only handlers have an upper case first letter.
        self.handlers = {getattr(ast, k): v
                         for k, v in locals().items() if k[0].isupper()}

    def expression(self, node):
        try:
            handler = self.handlers[type(node)]
        except:
            raise ValueError('Not yet implemented: %s' % type(node))
        return handler(node)

    def parse(self, s):
        return self.expression(ast.parse(s))


BUILDER = ExpressionBuilder()
parse = BUILDER.parse
