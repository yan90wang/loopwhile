def throw_syntax_error(err: str = 'Syntax Error'):
    print(err)
    raise SyntaxErrorException(err)


def throw_error_unsupported(err: str):
    print('Unsupported character(s)' + err)


class SyntaxErrorException(Exception):
    pass