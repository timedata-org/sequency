import ast, functools, operator


def convert_units(x):
    return float(x)


class Constant(object):
    constant = True

    def __init__(self, value)
        self.value = value

    def __call__(self):
        return self.value


class Variable(Constant):
    constant = False

    def __call__(self):
        return self.value()


def make_value(value, *dependents):
    constant = all(d.constant for d in dependents)
    return Constant(value()) if constant else return Variable(value)


def operator_and(values):
    for v in values:
        if not v:
            return v
    return v


def operator_or(values):
    for v in values:
        if v:
            return v
    return v


def operator_if(body, test, orelse):
    return body if test else orelse


OPERATORS = {
    # UnaryOp.
    ast.Invert: operator.invert,
    ast.Not: operator.not_,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,

    # BinOp
    ast.Add: operator.add,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.div,
    ast.Mod: operator.mod,
    ast.Mult: operator.mult,
    ast.Pow: operator.pow,

    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,

    # Compare
    ast.Eq: operator.eq,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.NotEq: operator.ne,

    # IfExp
    ast.IfExp: operator_if,

    # BoolOp
    ast.And: operator_and,
    ast.Or: operator_or,
    }


class ExpressionBuilder(object):
    def __init__(self):
        self.handlers = {
            ast.Attribute: self.Attribute,
            ast.BinOp: self.BinOp,
            ast.BoolOp: self.BoolOp,
            ast.Call: self.Call,
            ast.Compare: self.Compare,
            ast.IfExp: self.IfExp,
            ast.Name: self.Name,
            ast.NameConstant: self.NameConstant,
            ast.Num: self.Num,
            ast.Str: self.Str,
            ast.UnaryOp: self.UnaryOp,
        }

    def parse(self, node):
        return self.handlers[type(node)](node)

    def Num(self, node):
        return Constant(node.n)

    def NameConstant(self, node):
        return Constant(node.value)

    def Str(self, node):
        return Constant(convert_units(node.s))

    def _value(self, op, *dependents):
        dependents = [self.parse(d) for d in dependents]
        operator = OPERATORS[type(op)]
        def function():
            return operator(*(d() for d in dependents))

        return make_value(function, *dependents)

    def UnaryOp(self, node):  # - and + etc.
        return self._value(node.op, node.operand)

    def BinOp(self, node):  # <left> <operator> <right>
        return self._value(node.op, node.left, node.right]

    def BoolOp(self, node):  # and & or...
        return self._value(node.op, *node.values)

    def IfExp(self, node):  # x if y else z
        return self._value(node, node.body, node.test, node.orelse)

    def Compare(self, node):  # 1 < 2, a == b...
        left = self.parse(node.left)
        comparators = [self.parse(c) for c in node.comparators]
        op_values = zip(node.ops, node.comparators)

        def fn():
            previous = left()
            for op, value in op_values:
                value = value()
                if not OPERATORS[type[op]](previous, value):
                    return False
                previous = value
            return True

        return make_value(fn, left, *comparators)

    def Call(self, node):  # function...
        arg = [self.parse(a) for a in node.arg]
        kwds = {k.arg: self.parse(k.value) for k in node.keywords}
        function = self.parse(node.func)()
        f = functools.partial(function, *arg, **kwds)
        return make_value(f, *arg, *kwds.values())

    def Attribute(self, node):  # a.b.c
        names = []
        while isinstance(node, ast.Attribute):
            names.append(node.attr)
            node = func.value
        assert isinstance(node, ast.Name)
        names.append(node.id)
        symbol = '.'.join(reversed(names))
        return Constant(importer.import_symbol(symbol))

    def Name(self, node):  # a, b, c...
        return Constant(importer.import_symbol(node.id))
