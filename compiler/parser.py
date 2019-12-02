from compiler.AST import *
from compiler.tokens import Tokens, TOKENTYPES
from compiler.error_printer import throw_syntax_error


class Parser:
    '''
        Takes a list of tokens and creates AST
    '''

    def __init__(self):
        self.AST = None

    def create_AST(self, tokens):
        if len(tokens) >= 1:
            token = tokens.pop(0)
            if token.type == TOKENTYPES.get('def'):
                self.AST = self.create_and_check_definition_AST(tokens)
            else:
                throw_syntax_error(
                    "No function definition found, please define a Loop/While function with: def func(arguments)")
        else:
            throw_syntax_error(
                "No function definition found, please define a Loop/While function with: def func(arguments)")
        has_end = self.create_AST_nodes(self.AST, token, tokens)
        if has_end:
            throw_syntax_error('keyword END found without corresponding LOOP keyword')

    def create_AST_nodes(self, current_node, old_token, tokens) -> bool:
        while len(tokens) >= 1:
            current_token = tokens.pop(0)
            if current_token.type == TOKENTYPES.get(':='):
                if old_token.type == TOKENTYPES.get('variable'):
                    left = self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get('variable')])
                    operator = self.check_correct_token(self.eat_next_token(tokens),
                                                        [TOKENTYPES.get('+'), TOKENTYPES.get('-')])
                    right = self.check_correct_token(self.eat_next_token(tokens),
                                                     [TOKENTYPES.get('variable'), TOKENTYPES.get('number')])
                    operation = BinaryOperator(left, operator, right)
                    current_node.body.append(Assignment(current_token, old_token, operation))
                    self.check_semicolon_needed(tokens)
                else:
                    throw_syntax_error('Assignment missing variable to assign to')
            if current_token.type == TOKENTYPES.get('LOOP'):
                condition = self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get('variable')])
                loop_node = Loop(condition, current_token)
                self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get('DO')])
                has_end = self.create_AST_nodes(loop_node, current_token, tokens)
                if not has_end:
                    throw_syntax_error('No according END')
                current_node.body.append(loop_node)
                self.check_semicolon_needed(tokens)
            if current_token.type == TOKENTYPES.get('END'):
                return True
            if current_token.type != TOKENTYPES.get('variable') and current_token.type != TOKENTYPES.get(
                    ':=') and current_token.type != TOKENTYPES.get('LOOP') and current_token.type != TOKENTYPES.get(
                'END'):
                throw_syntax_error('Unmatched character(s) found: ' + current_token.value)
            old_token = current_token
        return False

    def check_semicolon_needed(self, tokens):
        token_after_next_token = None
        if len(tokens) >= 2:
            token_after_next_token = tokens[1]
        if token_after_next_token is not None:
            if token_after_next_token.type is not TOKENTYPES.get('END'):
                self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get(';')])

    def create_and_check_definition_AST(self, tokens):
        function_name = self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get('variable')])
        self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get('(')])
        input_params = []
        next_param = self.eat_next_token(tokens)
        while next_param.type is not TOKENTYPES.get(')') or None:
            if next_param.type is TOKENTYPES.get(','):
                next_param = self.eat_next_token(tokens)
            input_params.append(Variable(self.check_correct_token(next_param, [TOKENTYPES.get('variable')])))
            next_param = self.eat_next_token(tokens)
        if next_param.type is TOKENTYPES.get(')'):
            new_root = Definition(function_name, input_params)
        self.check_correct_token(self.eat_next_token(tokens), [TOKENTYPES.get(':')])
        return new_root

    def eat_next_token(self, tokens) -> Tokens:
        if (len(tokens) >= 1):
            return tokens.pop(0)
        else:
            throw_syntax_error('Missing character(s) or incomplete statement')

    def check_correct_token(self, token, expected_token_types: [str]) -> Tokens:
        for i in range(len(expected_token_types)):
            if (token.type == expected_token_types[i]):
                return token
        throw_syntax_error('Expected: ' + str(expected_token_types) + ' but actual: ' + token.value)
