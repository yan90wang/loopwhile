TOKENTYPES = {
    '(': 'OPEN_PARENS',
    ')': 'CLOSED_PARENS',
    '+': 'PLUS',
    '-': 'MINUS',
    ':=': 'ASSIGN',
    ';': 'COMPOSITION',
    ',': 'MULTI_INPUT',
    'number': 'NUMBER',
    'variable': 'VARIABLE',
    'def': 'DEFINITION',
    'LOOP':'LOOP',
    'DO': 'DO',
    'END': 'END',
    ':': 'DEFINITION_END'
}


class Tokens:
    '''
        A token is the smallest symbol that the parser can process
    '''

    def __init__(self, val: str, type: str):
        self.value = val
        self.type = type
