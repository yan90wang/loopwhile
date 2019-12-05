def throw_syntax_error(err: str = 'Syntax Error'):
    print(err)
    raise SyntaxErrorException(err)


def throw_error_unsupported(err: str):
    print('Unsupported character(s)' + err)

def throw_semantic_error(err: str):
    print(err)
    raise SemanticErrorException(err)

class SyntaxErrorException(Exception):
    pass

class SemanticErrorException(Exception):
    pass