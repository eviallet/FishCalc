from interpreter.token import Token, TokenType


class Error(Exception):
    def __init__(self, token, msg, line_content=''):
        self.token = token
        self.message = msg
        self.line_content = line_content

    def __str__(self):
        line = ''
        if self.token is not None and self.token.line != 1:
            line = '[line %s] ' % self.token.line
        line_content = ''
        if len(self.line_content) > 0:
            line_content = '\n\t%s' % self.line_content
        return '%s%s - %s%s' % \
               (line, type(self).__name__, self.message, line_content)

class MathError(Error): pass

class ParseError(Error): pass

class RuntimeError(Error): pass

class ScanError(Error):
    def __init__(self, msg, line):
        super(ScanError, self).__init__(Token(TokenType.EOF, '', None, line), msg)
