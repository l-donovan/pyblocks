from .utils import listify

class Block():
    def __init__(self):
        pass

class Program():
    def __init__(self, root_block):
        self.root_block = listify(root_block)

    def run(self):
        scope = {}
        for item in self.root_block:
            scope, result = item.run(scope)

class ForLoop(Block):
    def __init__(self, iterator, iterable, body):
        self.iterator = iterator
        self.iterable = iterable
        self.body = listify(body)

    def run(self, scope={}):
        for i in self.iterable:
            scope[self.iterator] = i
            for item in self.body:
                scope, result = item.run(scope)
        return scope, None

class WhileLoop(Block):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = listify(body)

    def run(self, scope={}):
        while (True):
            scope, result = self.condition.run(scope)
            if (not result):
                break
            for item in self.body:
                scope, result = item.run(scope)
        return scope, None

class Set(Block):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def run(self, scope={}):
        scope, literal = self.value.run(scope)
        scope[self.name] = literal
        return scope, None

class Get(Block):
    def __init__(self, name):
        self.name = name

    def run(self, scope={}):
        return scope, scope[self.name]

class Print(Block):
    def __init__(self, literal):
        self.literal = literal

    def run(self, scope={}):
        scope, value = self.literal.run(scope)

        if (type(value) is Literal):
            scope, value = value.run(scope)

        print(value, end='')

        return scope, None

class Compare(Block):
    def __init__(self, operator, value1, value2):
        self.operator = operator
        self.value1 = value1
        self.value2 = value2

    def run(self, scope={}):
        scope, v1 = self.value1.run(scope)

        if (type(v1) is Literal):
            scope, v1 = v1.run(scope)

        scope, v2 = self.value2.run(scope)

        if (type(v2) is Literal):
            scope, v2 = v2.run(scope)

        if (self.operator == '=='):
            result = v1 == v2
        elif (self.operator == '!='):
            result = v1 != v2
        elif (self.operator == '>'):
            result = v1 > v2
        elif (self.operator == '>='):
            result = v1 >= v2
        elif (self.operator == '<'):
            result = v1 < v2
        elif (self.operator == '<='):
            result = v1 <= v2
        else:
            result = None

        return scope, result

class If(Block):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = listify(body)

    def run(self, scope={}):
        scope, outcome = self.condition.run(scope)
        if (outcome):
            for item in self.body:
                scope, result = item.run(scope)
        return scope, outcome

class Else(Block):
    def __init__(self, body):
        self.body = listify(body)

    def run(self, scope={}):
        for item in self.body:
            item.run(scope)
        return scope, True

class ConditionSection(Block):
    def __init__(self, conditions):
        self.conditions = conditions

    def run(self, scope={}):
        for condition in self.conditions:
            outcome = condition.run(scope)
            if (outcome):
                break
        return scope, None

class Literal(Block):
    def __init__(self, value):
        self.value = value

    def run(self, scope={}):
        return scope, self.value

class Math(Block):
    def __init__(self, operator, args):
        self.operator = operator
        self.args = args

    def run(self, scope={}):
        new_args = []

        for arg in self.args:
            scope, result = arg.run(scope)
            if (type(result) is Literal):
                scope, result = result.run(scope)
            new_args.append(result)

        if (self.operator == '+'):
            out = Literal(sum(new_args))
        elif (self.operator == '-'):
            out = Literal(new_args[0] + sum([-arg for arg in new_args[1:]]))
        elif (self.operator == '*'):
            out = Literal(math.prod(new_args))
        elif (self.operator == '/'):
            out = Literal(new_args[0] / new_args[1])
        else:
            out = None

        return scope, out

class Return(Block):
    def __init__(self, item):
        self.item = item

    def run(self, scope={}):
        scope, result = self.item.run(scope)
        return scope, result

class FunctionHelper():
    def __init__(self, arg_names, body):
        self.arg_names = arg_names
        self.body = body

    def call(self, scope={}):
        for item in self.body:
            scope, result = item.run(scope)
        return scope, result

class Function(Block):
    def __init__(self, name, arg_names, body):
        self.name = name
        self.arg_names = arg_names
        self.body = listify(body)

    def run(self, scope={}):
        scope[self.name] = FunctionHelper(self.arg_names, self.body)
        return scope, None

class Call(Block):
    def __init__(self, fn_name, args):
        self.fn_name = fn_name
        self.args = listify(args)

    def run(self, scope={}):
        fn = scope[self.fn_name]
        fn_scope = scope

        for i, v in enumerate(fn.arg_names):
            fn_scope[v] = self.args[i]

        fn_scope, result = fn.call(fn_scope)

        return scope, result
