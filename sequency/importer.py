# From BiblioPixel

import importlib


def import_symbol(typename):
    """Import a module or typename within a module from its name."""
    try:
        return importlib.import_module(typename)

    except ImportError:
        parts = typename.split('.')
        if len(parts) == 1:
            built = __builtin__.get(typename)
            if built:
                return built
            raise
        typename = parts.pop()

        # Call import_module recursively.
        namespace = import_symbol('.'.join(parts))
        return getattr(namespace, typename)


def make_object(*args, typename, **kwds):
    """Make an object from a symbol."""
    return import_symbol(typename)(*args, **kwds)
