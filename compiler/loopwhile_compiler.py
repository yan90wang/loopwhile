from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.AST import *
from compiler.tokens import *
from compiler.error_printer import *

class LoopWhileCompiler:

    def compile(self, txt_file, parameters):
        '''
            Takes an input the txt_file name containing the loop/While program code and the parameters (if any) as
            a list

            example:
            LoopWhileCompiler.compile(addition.txt, [1,2]
            result = 3
        '''
        print('#######################')
        code_file = open(txt_file, "r")
        lexer = Lexer(code_file.read())
        parser = Parser()
        parser.create_AST(lexer.create_tokens())
        variables = self.get_all_defined_variables(parser.AST, {'x0': 0})
        self.check_variable_names(variables)
        variables = self.set_initial_variable_values(parser.AST, variables, parameters)
        self.generate_code(parser.AST, variables)
        print("Result: " + str(variables['x0']))
        print('#######################')

    def generate_code(self, current_node, variables):
        if isinstance(current_node, Definition):
            for statement in current_node.body:
                self.generate_code(statement, variables)
        if isinstance(current_node, Assignment):
            left_value = 0
            right_value = 0
            if current_node.right.left.type is TOKENTYPES.get('variable'):
                left_value = variables[current_node.right.left.value]
            else:
                left_value = int(current_node.right.left.value)
            if current_node.right.right.type is TOKENTYPES.get('variable'):
                right_value = variables[current_node.right.right.value]
            else:
                right_value = int(current_node.right.right.value)
            if current_node.right.token.type is TOKENTYPES.get('+'):
                variables[current_node.left.value] = left_value + right_value
            else:
                variables[current_node.left.value] = left_value - right_value
        if isinstance(current_node, Loop):
            for i in range(variables[current_node.condition.value]):
                for statement in current_node.body:
                    self.generate_code(statement, variables)
        if isinstance(current_node, While):
            while variables[current_node.condition.left.value] != int(current_node.condition.right.value):
                for statement in current_node.body:
                    self.generate_code(statement, variables)

    def get_all_defined_variables(self, current_node, variables):
        if isinstance(current_node, Definition):
            for var in variables:
                if var not in variables:
                    variables[var.token.value] = 0
            for statement in current_node.body:
                variables = self.get_all_defined_variables(statement, variables)
        if isinstance(current_node, Assignment):
            var_to = current_node.left.value
            var_left = current_node.right.left
            var_right = current_node.right.right
            if var_to not in variables:
                variables[var_to] = 0
            if var_left.type is not TOKENTYPES.get('number'):
                if var_left.value not in variables:
                    variables[var_left.value] = 0
            if var_right.type is not TOKENTYPES.get('number'):
                if var_right.value not in variables:
                    variables[var_right.value] = 0
        if isinstance(current_node, Loop):
            for statement in current_node.body:
                variables = self.get_all_defined_variables(statement, variables)
        if isinstance(current_node, While):
            for statement in current_node.body:
                variables = self.get_all_defined_variables(statement, variables)
        return variables

    def set_initial_variable_values(self, DefinitionAST, variables, parameters):
        i = 0
        if len(parameters) != len(DefinitionAST.left):
            throw_semantic_error('Missing input parameters')
        for params in DefinitionAST.left:
            variables[params.token.value] = parameters[i]
            i += 1
        return variables

    def check_variable_names(self, variables):
        for key in variables:
            if len(key) != 2:
                if key[0] != 'x' or not key[1].isdigit():
                    throw_syntax_error('Variables have to be of the form xn, but variable was: ' + key)

