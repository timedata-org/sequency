import ast, operator


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



OPERATORS = {
    # UnaryOp.
    ast.Invert: operator.invert,
    ast.Not: operator.not_,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,

    # BinOp
    ast.Add: operator.add,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Mult: operator.mul,
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
    ast.Is: (lambda x, y: x == y),
    ast.IsNot: (lambda x, y: x is y),
    ast.In: operator_in,
    ast.NotIn: operator_not_in,

    # BoolOp
    ast.And: operator_and,
    ast.Or: operator_or,
}


def get(op):
    try:
        return OPERATORS[type(op)]
    except:
        raise ValueError('Don\'t understand class %s' % type(op))
