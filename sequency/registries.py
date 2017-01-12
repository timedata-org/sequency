"""A function that is marked "volatile" is one that might give different values
if it is called again.

Examples include clock functions and functions that get a mutable state from the
system.

We extend the builtins with our own list of "global" functions that are
recognized everywhere.
"""

VOLATILES = set()
BUILTINS = dict(__builtins__)


def volatile(f):
    """A decorator to show a function is volatile.
    """
    VOLATILES.add(f)
    return f


def builtin(f, name=None):
    name = name or f.__name__
    assert name not in BUILTINS
    BUILTINS[name] = f
    return f
