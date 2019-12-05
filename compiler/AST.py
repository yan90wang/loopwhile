class AST:
    '''
            Simple abstract syntax tree
    '''

    def __init__(self):
        pass


class BinaryOperator(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        self.token = operator

class Assignment(AST):
    def __init__(self, assignment, variable_to, binary_operator):
        self.token = assignment
        self.left = variable_to
        self.right = binary_operator

class Constant(AST):
    def __init__(self, number):
        self.token = number


class Variable(AST):
    def __init__(self, variable):
        self.token = variable


class Loop(AST):
    def __init__(self, condition, loop):
        self.condition = condition
        self.body = []
        self.token = loop


class Definition(AST):
    def __init__(self, function_name, parameters):
        self.left = parameters
        self.token = function_name
        self.body = []

class While(AST):
    def __init__(self, condition, while_token):
        self.condition = condition
        self.body = []
        self.token = while_token

class NotEquals(AST):
    def __init__(self, left, not_equals, right):
        self.left = left
        self.right = right
        self.token = not_equals