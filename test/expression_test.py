import unittest
from sequency import expression


def importer(s):
    return lambda *a, **k: s


BUILDER = expression.ExpressionBuilder(importer)
parse = BUILDER.parse


class BasicTest(unittest.TestCase):
    def test_trivial(self):
        self.assertEqual(parse('')(), None)
