"""
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
addition       → multiplication ( ( "-" | "+" ) multiplication )* ;
multiplication → exponent ( ( "/" | "*" ) exponent )* ;
exponent       → unary ( "^" unary )* ;
unary          → ( "!" | "-" ) unary | primary ;
primary        → NUMBER | STRING | IDENTIFIER | "false" | "true" | "(" expression ")" ;
"""

from interpreter.environment import Environment
from interpreter.token import keywords
from interpreter.expr import *
from interpreter.files import Files


class Parser:

    def __init__(self):
        self.tokens = []
        self.current = 0
        self.environment = Environment()

    def parse(self, tokens):
        self.tokens = tokens
        self.current = 0
        exprs = []

        while not self.is_at_end():
            try:
                exprs.append(self.expression())
                if not self.is_at_end():
                    if self.match(TokenType.SEMICOLON):
                        exprs[len(exprs)-1].mute = True
                    if not self.is_at_end() and not self.match(TokenType.NEWLINE):
                        raise ParseError(self.peek(), "Expect newline between statements")
            except ParseError as err:
                exprs.append(err)
                self.synchronize()
        return exprs

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.addition()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Binary(expr, operator, right)

        return expr

    def addition(self):
        expr = self.multiplication()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Binary(expr, operator, right)

        return expr

    def multiplication(self):
        expr = self.exponent()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.exponent()
            expr = Binary(expr, operator, right)

        return expr

    def exponent(self):
        expr = self.conversion()
        while self.match(TokenType.EXPO):
            operator = self.previous()
            right = self.conversion()
            expr = Binary(expr, operator, right)

        return expr

    def conversion(self):
        expr = self.unary()
        while self.match(TokenType.ARROW):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            # NUMBER 'e' -? expr
            # 1e3 or 2.5e-6
            if self.peek().lexeme.startswith('e'):
                left = self.previous().literal
                right = self.peek().lexeme[1:]
                if len(right) < 1:
                    self.advance()
                    self.consume(TokenType.MINUS, 'Expect expression after "e"')
                    right = - self.expression().evaluate()
                right = float(right)

                self.advance()
                return Literal(left * pow(10, right))
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        if self.match(TokenType.IDENTIFIER):
            name = self.previous().lexeme
            if self.match(TokenType.EQUAL):
                try:
                    value = self.expression().evaluate()
                except MathError as err:
                    return err
                var = Variable(name, value)
                self.environment.add_var(var)
                return var
            else:
                try:
                    return Literal(self.environment.vars[name])
                except KeyError:
                    raise ParseError(self.peek(), "Undefined variable : " + self.previous().lexeme)

        if self.is_function():
            name = self.peek().lexeme
            self.advance()
            if name in keywords:
                args = []
                if self.match(TokenType.LEFT_PAREN):
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
                return Function(name, args)

        if self.match(TokenType.ANSWER):
            try:
                return Literal(self.environment.vars['ans'])
            except KeyError:
                raise ParseError(self.peek(), "Evaluate an expression first.")

        if self.match(TokenType.SAVE, TokenType.LOAD):
            return Files(self.previous())

        raise ParseError(self.peek(), "Expect expression.")

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise ParseError(self.peek(), message)

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def is_function(self):
        return TokenType.FIRST_FUNC.value <= self.peek().type.value <= TokenType.LAST_FUNC.value

    def check(self, token_type):
        if self.is_at_end():
            return False
        else:
            if self.peek().type == token_type:
                return True
            return False

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def peek_next(self):
        if self.current+1 < len(self.tokens):
            return None
        return self.tokens[self.current+1]

    def previous(self):
        return self.tokens[self.current-1]

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE:
                return
            self.advance()
