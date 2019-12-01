import unittest
from compiler.lexer import Lexer
from compiler.tokens import Tokens, TOKENTYPES

class TestTokenCreation(unittest.TestCase):
#### Helper Functions ####
    def validate_tokens(self, generated_tokens, tokens):
        for i in range(len(tokens)):
            self.assertEqual(tokens[i].type, generated_tokens[i].type)
            self.assertEqual(tokens[i].value, generated_tokens[i].value)

#### Program Definition ####
    def test_one_input_parameter(self):
        program_definition = 'TestFunction(x1)'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('TestFunction', TOKENTYPES.get('variable')), Tokens('(', TOKENTYPES.get('(')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens(')', TOKENTYPES.get(')'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_three_input_parameters(self):
        program_definition = 'TestFunction(x1, x2, x3)'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('TestFunction', TOKENTYPES.get('variable')), Tokens('(', TOKENTYPES.get('(')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens(',', TOKENTYPES.get(',')),
                  Tokens('x2', TOKENTYPES.get('variable')), Tokens(',', TOKENTYPES.get(',')),
                  Tokens('x3', TOKENTYPES.get('variable')), Tokens(')', TOKENTYPES.get(')'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_valid_definition(self):
        program_definition = 'def MyFunc(x1):'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('def', TOKENTYPES.get('def')), Tokens('MyFunc', TOKENTYPES.get('variable')),
                  Tokens('(', TOKENTYPES.get('(')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens(')', TOKENTYPES.get(')')), Tokens(':', TOKENTYPES.get(':'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_assignment_to_variable(self):
        program_definition = 'x2:=312'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('312', TOKENTYPES.get('number'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_LOOP(self):
        program_definition = 'LOOP x1 DO END'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('LOOP', TOKENTYPES.get('LOOP')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens('DO', TOKENTYPES.get('DO')), Tokens('END', TOKENTYPES.get('END'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_nested_LOOP(self):
        program_definition = 'LOOP x1 DO LOOP x2 DO END END'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('LOOP', TOKENTYPES.get('LOOP')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens('DO', TOKENTYPES.get('DO')), Tokens('LOOP', TOKENTYPES.get('LOOP')),
                  Tokens('x2', TOKENTYPES.get('variable')), Tokens('DO', TOKENTYPES.get('DO')),
                  Tokens('END', TOKENTYPES.get('END')), Tokens('END', TOKENTYPES.get('END'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_minus_operation(self):
        program_definition = 'x2 := x1 - 99'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens('-', TOKENTYPES.get('-')),
                  Tokens('99', TOKENTYPES.get('number'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_plus_operation(self):
        program_definition = 'x2 := x1 + 99'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+')),
                  Tokens('99', TOKENTYPES.get('number'))]
        self.validate_tokens(generated_tokens, tokens)

    def test_program_execution(self):
        program_definition = 'MyProgram;Bloop1 ; Floop'
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = [Tokens('MyProgram', TOKENTYPES.get('variable')), Tokens(';', TOKENTYPES.get(';')),
                  Tokens('Bloop1', TOKENTYPES.get('variable')), Tokens(';', TOKENTYPES.get(';')),
                  Tokens('Floop', TOKENTYPES.get('variable'))]
        self.validate_tokens(generated_tokens, tokens)

 #### General Cases and negative tests ####
    def test_empty_word(self):
        program_definition = '   '
        self.lexer = Lexer(program_definition)
        generated_tokens = self.lexer.create_tokens()
        tokens = []
        self.assertEqual(tokens, generated_tokens)

    # def test_invalid_character(self):
    #     program_definition = '#'
    #     self.lexer = Lexer(program_definition)
    #     # TODO

if __name__ == '__main__':
    unittest.main()
