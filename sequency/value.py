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


def Value(function, *dependents):
    # Returns a Constant if all dependents are constant, otherwise a
    # Variable.
    constant = all(d.constant for d in dependents)
    return Constant(function()) if constant else Variable(function)
