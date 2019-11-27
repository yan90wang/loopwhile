from compiler.tokens import Tokens, TOKENTYPES
from compiler.error_printer import throw_error_unsupported


class Lexer:
    '''
        Lexer creates a list of tokens out of plain text strings
    '''

    def __init__(self, input_code):
        self.full_code = input_code

    def create_tokens(self) -> [Tokens]:
        token_list = []
        identifier = ''
        for current_char in self.full_code:
            if current_char.isalnum():
                identifier += current_char
            elif current_char == '(' or ')' or '+' or '-' or ':' or '=' or ' ' or ',' or ';':
                self.create_multi_char_tokens(identifier, token_list, current_char)
                identifier = ''
                if current_char == ':':
                    identifier = current_char
                elif current_char != ' ' and current_char != '=':
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
            elif identifier == 'def' or identifier == 'LOOP' or identifier == 'END' or identifier == 'DO':
                token_list.append(Tokens(identifier, TOKENTYPES.get(identifier)))
            elif identifier.isdigit():
                token_list.append(Tokens(identifier, TOKENTYPES.get('number')))
            elif identifier.isalnum():
                token_list.append(Tokens(identifier, TOKENTYPES.get('variable')))
            else:
                throw_error_unsupported(identifier)

if __name__ == '__main__':
    program_definition = 'def MyFunc(x1):'
    lexer = Lexer(program_definition)
    generated_tokens = lexer.create_tokens()
    for i in range(len(generated_tokens)):
        print(i)
        print(generated_tokens[i].value + '   ' + generated_tokens[i].type)
