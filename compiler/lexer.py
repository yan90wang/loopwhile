from compiler.tokens import Tokens, TOKENTYPES
from compiler.error_printer import throw_error_unsupported


class Lexer:
    '''
        Lexical analysis of code by creating tokens out of loop/while code,
        followed by syntax checking through an Abstract Syntax Tree.
    '''

    def __init__(self, input_code):
        self.full_code = input_code
        self.AST = []

    def create_tokens(self) -> [Tokens]:
        token_list = []
        identifier = ''
        for current_char in self.full_code:
            if current_char.isalnum():
                identifier += current_char
            elif current_char == '(' or ')' or '+' or '-' or ':' or '=' or ' ' or ',' or ';' or '\n':
                self.create_multi_char_tokens(identifier, token_list, current_char)
                identifier = ''
                if current_char == ':':
                    identifier = current_char
                elif current_char != ' ' and current_char != '=' and current_char != '\n':
                    token_list.append(Tokens(current_char, TOKENTYPES.get(current_char)))
        if identifier != '':
            self.create_multi_char_tokens(identifier, token_list, '')
        return token_list

    def create_multi_char_tokens(self, identifier, token_list, current_char):
        if identifier != '':
            if identifier == ':':
                if current_char == '=':
                    token_list.append(Tokens(':=', TOKENTYPES.get(':=')))
                else:
                    token_list.append(Tokens(identifier, TOKENTYPES.get(identifier)))
            elif identifier == 'def' or identifier == 'LOOP' or identifier == 'END' or identifier == 'DO' or identifier == 'WHILE' or identifier == 'not':
                token_list.append(Tokens(identifier, TOKENTYPES.get(identifier)))
            elif identifier.isdigit():
                token_list.append(Tokens(identifier, TOKENTYPES.get('number')))
            elif identifier.isalnum():
                token_list.append(Tokens(identifier, TOKENTYPES.get('variable')))
            else:
                throw_error_unsupported(identifier)
