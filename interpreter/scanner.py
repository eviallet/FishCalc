from interpreter.token import keywords
from interpreter.errors import *

class Scanner:

    def __init__(self):
        self.start = 0
        self.current = 0
        self.line = 1

        self.source = ""
        self.tokens = []
        self.had_error = False
        self.skip_next_newline = False

    def scan(self, source: str):
        self.start = 0
        self.current = 0
        self.line = 1

        self.source = source
        self.tokens = []
        self.had_error = False
        self.skip_next_newline = False

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens, self.had_error

    def scan_token(self):
        c = self.advance()

        if self.skip_next_newline:
            self.skip_next_newline = False
            if c == '\n': return  # ignore it
            else: self.scan_error("Expected newline after '\\'.")

        # punctuation
        if   c == '(':  self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':  self.add_token(TokenType.RIGHT_PAREN)
        elif c == ',':  self.add_token(TokenType.COMMA)
        elif c == ':':  self.add_token(TokenType.COLON)

        # operators
        elif c == '-':
            if self.match('>'):
                self.add_token(TokenType.ARROW)
            else:
                self.add_token(TokenType.MINUS)
        elif c == '⇒': self.add_token(TokenType.ARROW)
        elif c == '/':
            if self.match('/'):  # comment
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '+':  self.add_token(TokenType.PLUS)
        elif c == '*':  self.add_token(TokenType.STAR)
        elif c == '%':  self.add_token(TokenType.PERCENT)
        elif c == '^':  self.add_token(TokenType.EXPO)
        elif c == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == '<':
            if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == '√': self.add_token(TokenType.SQRT)

        # useless characters
        elif c == ' ': pass
        elif c == '\r': pass
        elif c == '\t': pass

        # new line
        elif c == '\\': self.skip_next_newline = True
        elif c == '\n': self.add_token(TokenType.NEWLINE)

        # mute result
        elif c == ';': self.add_token(TokenType.SEMICOLON)

        # literals
        elif c == '"': self.string()

        elif self.is_digit(c): self.number()
        elif self.is_alpha(c): self.identifier()

        # other
        else:
            self.scan_error("Unexpected character : " + c)

    def is_at_end(self):
        return self.current >= len(self.source)

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    # CHAR BY CHAR SCANNING
    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current+1]

    def match(self, c):
        if not self.is_at_end() and self.source[self.current] != c:
            return False
        self.current += 1
        return True

    # LITERALS
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.scan_error("Unterminated string : %s" % self.source[self.start:self.current])
            return

        # consume the closing "
        self.advance()

        # trim the quotes
        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # look for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # consume the '.'
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        if text in keywords:
            token_type = keywords[text]
        else:
            token_type = TokenType.IDENTIFIER

        self.add_token(token_type)

    # CHARACTER IDENTIFICATION
    @staticmethod
    def is_digit(c):
        return '0' <= c <= '9'

    @staticmethod
    def is_alpha(c):
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def is_alphanumeric(self, c):
        return self.is_digit(c) or self.is_alpha(c)

    def scan_error(self, message):
        raise ScanError(message, self.line)

