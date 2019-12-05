TOKENTYPES = {
    '(': 'OPEN_PARENS',
    ')': 'CLOSED_PARENS',
    '+': 'PLUS',
    '-': 'MINUS',
    ':=': 'ASSIGN',
    ';': 'SEMICOLON',
    ',': 'COLON',
    'number': 'NUMBER',
    'variable': 'VARIABLE',
    'def': 'DEFINITION',
    'LOOP': 'LOOP',
    'DO': 'DO',
    'END': 'END',
    ':': 'DEFINITION_END',
    'WHILE': 'WHILE',
    'not': 'not'
}


class Tokens:
    '''
        A token is the smallest symbol that the parser can process
    '''

    def __init__(self, val: str, token_type: str):
        self.value = val
        self.type = token_type
