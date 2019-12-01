import unittest
from compiler.error_printer import SyntaxErrorException
from compiler.parser import Parser
from compiler.tokens import *


class TestSyntax(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.correct_definition = [Tokens('def', TOKENTYPES.get('def')),
                                   Tokens('function1', TOKENTYPES.get('variable')),
                                   Tokens('(', TOKENTYPES.get('(')), Tokens('x1', TOKENTYPES.get('variable')),
                                   Tokens(')', TOKENTYPES.get(')')), Tokens(':', TOKENTYPES.get(':'))]

    def expect_exception(self, tokens):
        with self.assertRaises(SyntaxErrorException):
            self.parser.create_AST(self.correct_definition + tokens)

    def test_assignment_without_operator(self):
        #  parsing x2:=312
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('312', TOKENTYPES.get('number'))]
        self.expect_exception(tokens)

    def test_assignment_without_constant(self):
        #  parsing x2:= x3 +
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x3', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+'))]
        self.expect_exception(tokens)

    def test_assignment_without_constant_in_chained_assignment(self):
        #  parsing x2:= x3 + x3 := x1 + 4
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x3', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+')),
                  Tokens('x3', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+')),
                  Tokens('4', TOKENTYPES.get('number'))]
        self.expect_exception(tokens)

    def test_assignment_without_semicolon(self):
        #  parsing x2:= x3 + 3 x2 := x1 + 120
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x3', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+')),
                  Tokens('3', TOKENTYPES.get('number')), Tokens('x2', TOKENTYPES.get('variable')),
                  Tokens(':=', TOKENTYPES.get(':=')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens('+', TOKENTYPES.get('+')), Tokens('120', TOKENTYPES.get('number'))]
        self.expect_exception(tokens)

    def test_assignment_with_semicolon(self):
        #  parsing x2:= x3 + 3; x2 := x1 + 120
        tokens = [Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x3', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+')),
                  Tokens('3', TOKENTYPES.get('number')), Tokens(';', TOKENTYPES.get(';')),
                  Tokens('x2', TOKENTYPES.get('variable')), Tokens(':=', TOKENTYPES.get(':=')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens('+', TOKENTYPES.get('+')),
                  Tokens('120', TOKENTYPES.get('number'))]
        self.parser.create_AST(self.correct_definition + tokens)
        self.assertEqual(len(self.parser.AST.body), 2)

    def test_loop_with_one_statement(self):
        #  parsing loop x1 do x2 := x2 + 5 end
        tokens = [Tokens('LOOP', TOKENTYPES.get('LOOP')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens('DO', TOKENTYPES.get('DO')), Tokens('x2', TOKENTYPES.get('variable')),
                  Tokens(':=', TOKENTYPES.get(':=')), Tokens('x2', TOKENTYPES.get('variable')),
                  Tokens('+', TOKENTYPES.get('+')), Tokens('5', TOKENTYPES.get('number')),
                  Tokens('END', TOKENTYPES.get('END'))]
        self.parser.create_AST(self.correct_definition + tokens)
        self.assertEqual(len(self.parser.AST.body), 1)


class TestSyntaxFunctionDefinition(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def expect_exception(self, tokens):
        with self.assertRaises(SyntaxErrorException):
            self.parser.create_AST(tokens)

    def test_definition_without_def(self):
        #  parsing function1(x1):
        tokens = [Tokens('function1', TOKENTYPES.get('variable')), Tokens('(', TOKENTYPES.get('(')),
                  Tokens('x1', TOKENTYPES.get('variable')), Tokens(')', TOKENTYPES.get(')'))]
        self.expect_exception(tokens)

    def test_definition_without_colon_at_end(self):
        #  parsing def function1(x1)
        tokens = [Tokens('def', TOKENTYPES.get('def')), Tokens('function1', TOKENTYPES.get('variable')),
                  Tokens('(', TOKENTYPES.get('(')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens(')', TOKENTYPES.get(')'))]
        self.expect_exception(tokens)

    def test_correct_definition(self):
        #  parsing def function1(x1):
        tokens = [Tokens('def', TOKENTYPES.get('def')), Tokens('function1', TOKENTYPES.get('variable')),
                  Tokens('(', TOKENTYPES.get('(')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens(')', TOKENTYPES.get(')')), Tokens(':', TOKENTYPES.get(':'))]
        self.parser.create_AST(tokens)
        self.assertEqual(self.parser.AST.token.value, 'function1')
        # TODO make better check here

    def test_correct_definition_with_multiple_input(self):
        #  parsing def function2(x1,x2,x3):
        tokens = [Tokens('def', TOKENTYPES.get('def')), Tokens('function2', TOKENTYPES.get('variable')),
                  Tokens('(', TOKENTYPES.get('(')), Tokens('x1', TOKENTYPES.get('variable')),
                  Tokens(',', TOKENTYPES.get(',')), Tokens('x2', TOKENTYPES.get('variable')),
                  Tokens(',', TOKENTYPES.get(',')), Tokens('x3', TOKENTYPES.get('variable')),
                  Tokens(')', TOKENTYPES.get(')')), Tokens(':', TOKENTYPES.get(':'))]
        self.parser.create_AST(tokens)
        self.assertEqual(len(self.parser.AST.left), 3)
        self.assertEqual(self.parser.AST.left[0].token.value, 'x1')
        self.assertEqual(self.parser.AST.left[1].token.value, 'x2')
        self.assertEqual(self.parser.AST.left[2].token.value, 'x3')


if __name__ == '__main__':
    unittest.main()
