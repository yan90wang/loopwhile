from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.AST import *

class LoopWhileCompiler:

    def compile(self, txt_file, parameters):
        '''
            Takes an input the txt_file name containing the loop/While program code and the parameters (if any) as
            a list

            example:
            LoopWhileCompiler.compile(addition.txt, [1,2]
            result = 3
        '''
        code_file = open(txt_file, "r")
        lexer = Lexer(code_file.read())
        parser = Parser()
        parser.create_AST(lexer.create_tokens())
        variables = self.set_initial_variable_values(AST, parameters)
        self.generate_code(parser.AST, parameters)

    def generate_code(self, AST, parameters) -> int:
        current_node = AST
        result = 0
        while current_node is not None:
            if isinstance(current_node, Definition):
                for statement in current_node.body:
                    self.generate_code(statement, parameters)
            if isinstance(current_node, Assignment):
                self.set_variable(current_node.left, current_node.right)
                current_node = None
            if isinstance(current_node, Loop):
                for i in range(len(self.get_variable_value(current_node.condition))):
                    for statement in current_node.body:
                        self.generate_code(statement, parameters)
        return result



