from interpreter.expr import Function


class Environment:

    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def add_var(self, var):
        self.vars[var.name] = var.value

    def add_func(self, name, expr, *args):
        self.funcs[name] = Function(expr, args)

