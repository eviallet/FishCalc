"""
program     → declaration* EOF ;
declaration → varDecl | statement ;
varDecl     → IDENTIFIER ( "=" expression )? NEWLINE ;
statement   → expression NEWLINE ;
expression  → literal
            | unary
            | binary
            | grouping ;
literal     → NUMBER | STRING | "true" | "false" ;
grouping    → "(" expression ")" ;
unary       → ( "-" | "!" ) expression ;
binary      → expression operator expression ;
operator    → "==" | "!=" | "<" | "<=" | ">" | ">=" | "+"  | "-"  | "*" | "/" ;
"""

from abc import ABC, abstractmethod
from math import *
from interpreter.errors import *


def ast(expr):
    def __init__(self, *values):
        self.mute = False
        params = expr.template.split(',')
        for i in range(0, len(values)):
            setattr(self, params[i].replace(' ', ''), values[i])

    expr.__init__ = __init__
    return expr


def parenthesize(*exprs):
    res = '( '
    for expr in exprs:
        if isinstance(expr, str):
            res += expr + ' '
        else:
            res += expr.to_str() + ' '
    res += ')'
    return res


def get_type(obj):
    text = str(type(obj))
    return text[text.index("'") + 1:text.index("'", text.index("'") + 1)]


class Expr(ABC):
    @abstractmethod
    def to_str(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    def __str__(self):
        return self.to_str()

    @staticmethod
    def check_operand(operator, operand):
        if not isinstance(operand, float):
            raise RuntimeError(operator, "Operand must be a number")

    @staticmethod
    def check_operands(operator, operand1, operand2):
        if not isinstance(operand1, float) and not isinstance(operand2, float):
            raise RuntimeError(operator, "Operand must be a number")


@ast
class Binary(Expr):
    template = "left, operator, right"  # expr + expr

    def to_str(self):
        return parenthesize(self.operator.lexeme, self.left, self.right)

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if self.operator.type == TokenType.MINUS:
            return left - right
        try:
            if self.operator.type == TokenType.SLASH:
                return left / right
        except ZeroDivisionError:
            raise MathError(self.operator, "Division by zero.")
        if self.operator.type == TokenType.STAR:
            return left * right
        if self.operator.type == TokenType.EXPO:
            return pow(left, right)
        if self.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(self.operator, "Cannot add %s with %s." % (get_type(left), get_type(right)))
        if self.operator.type == TokenType.ARROW:
            if not isinstance(left, float):
                raise RuntimeError(self.operator, "Cannot convert non float type.")
            print(right)
            if (right != 'deg') and (right != 'rad'):
                raise RuntimeError(self.operator, "Can only convert to deg or rad.")
            if right == 'deg':
                return left*180/pi
            elif right == 'rad':
                return left*pi/180
            # TODO add other conversion types

        if self.operator.type == TokenType.GREATER:
            return left > right
        if self.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        if self.operator.type == TokenType.LESS:
            return left < right
        if self.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        if self.operator.type == TokenType.BANG_EQUAL:
            return left != right
        if self.operator.type == TokenType.EQUAL_EQUAL:
            return left == right

        return None


@ast
class Function(Expr):
    template = "func, args"  # func is a kw, arg is an expr

    def to_str(self):
        pass

    def evaluate(self):
        try:
            # CONSTANTS
            if self.func == 'pi':
                self.check_args_count(0)
                return pi
            elif self.func == 'q':
                self.check_args_count(0)
                return 1.602176634*pow(10, -19)
            elif self.func == 'kb':
                self.check_args_count(0)
                return 1.380649*pow(10, -23)
            elif self.func == 'h':
                self.check_args_count(0)
                return 6.62607015*pow(10, -34)
            elif self.func == 'c':
                self.check_args_count(0)
                return 299792458

            # CONVERSION
            elif self.func == "deg" or self.func == "rad":
                self.check_args_count(0)
                return self.func

            # FUNCTIONS
            # TODO second arg : 'deg' or 'rad'
            elif self.func == 'cos':
                self.check_args_count()
                return cos(self.args[0].evaluate())
            elif self.func == 'acos':
                self.check_args_count()
                return acos(self.args[0].evaluate())
            elif self.func == 'cosh':
                self.check_args_count()
                return cosh(self.args[0].evaluate())
            elif self.func == 'sin':
                self.check_args_count()
                return sin(self.args[0].evaluate())
            elif self.func == 'asin':
                self.check_args_count()
                return asin(self.args[0].evaluate())
            elif self.func == 'sinh':
                self.check_args_count()
                return sinh(self.args[0].evaluate())
            elif self.func == 'tan':
                self.check_args_count()
                return tan(self.args[0].evaluate())
            elif self.func == 'atan':
                self.check_args_count()
                return atan(self.args[0].evaluate())
            elif self.func == 'tanh':
                self.check_args_count()
                return tanh(self.args[0].evaluate())
            elif self.func == 'exp':
                self.check_args_count()
                return exp(self.args[0].evaluate())
            elif self.func == '√' or self.func == 'sqrt':
                if self.check_args_range(1, 2) == 2:
                    return pow(self.args[0].evaluate(), 1/self.args[1].evaluate())
                return sqrt(self.args[0].evaluate())
            elif self.func == 'ln':
                self.check_args_count()
                return log(self.args[0].evaluate(), e)
            elif self.func == 'log':
                self.check_args_count()
                return log10(self.args[0].evaluate())

        except ValueError:
            raise MathError(Token(TokenType.FIRST_FUNC, self.func, None, 1), "Math domain error.")

    def check_args_count(self, nb=1):
        print(len(self.args))
        if len(self.args) == nb:
            return True
        else:
            if nb == 0:
                raise ParseError(Token(TokenType.FIRST_FUNC, self.func, None, 1),
                                 "%s should have no parameters" % self.func)
            else:
                plural = ''
                if nb > 1: plural = 's'
                raise ParseError(Token(TokenType.FIRST_FUNC, self.func, None, 1),
                                 "%s should have %s parameter%s" % (self.func, nb, plural))

    def check_args_range(self, minimum, maximum):
        if not (minimum <= len(self.args) <= maximum):
            raise ParseError(Token(TokenType.FIRST_FUNC, self.func, None, 1),
                             "%s should have %s or %s parameters" % (self.func, minimum, maximum))
        return len(self.args)

@ast
class Grouping(Expr):
    template = "expression"  # ( expr )

    def to_str(self):
        return parenthesize("group", self.expression)

    def evaluate(self):
        return self.expression.evaluate()


@ast
class Literal(Expr):
    template = "value"  # "abc", 12.3, true

    def to_str(self):
        return self.value.__str__()

    def evaluate(self):
        return self.value


@ast
class Unary(Expr):
    template = "operator, right"  # - expr

    def to_str(self):
        return parenthesize(self.operator.lexeme, self.right)

    def evaluate(self):
        right = self.right.evaluate()

        if self.operator.type == TokenType.MINUS:
            return -right
        elif self.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

        return None

    @staticmethod
    def is_truthy(obj):
        if obj is None or False:
            return False
        return True


@ast
class Variable(Expr):
    template = "name, value"

    def to_str(self):
        return self.name + " = " + self.value.__str__()

    def evaluate(self):
        return self.value
