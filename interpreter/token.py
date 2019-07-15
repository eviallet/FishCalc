from enum import Enum


class TokenType(Enum):
    # PUNCTUATION
    LEFT_PAREN = 0       # (
    RIGHT_PAREN = 1      # )
    COMMA = 2            # ,
    DOT = 3              # .
    COLON = 4            # :
    SEMICOLON = 5       # ;
    NEWLINE = 6          # \n

    # OPERATORS
    MINUS = 10           # -
    PLUS = 11            # +
    SLASH = 12           # /
    STAR = 13            # *
    PERCENT = 14         # %
    EXPO = 15            # ^
    ARROW = 16           # ->
    EQUAL = 17           # =
    BANG = 18            # !
    BANG_EQUAL = 19      # !=
    EQUAL_EQUAL = 20     # ==
    GREATER = 21         # >
    GREATER_EQUAL = 22   # >=
    LESS = 23            # <
    LESS_EQUAL = 24      # <=

    # LITERALS
    IDENTIFIER = 30
    STRING = 31
    NUMBER = 32

    # KEYWORDS
    FIRST_FUNC = 40
    PI = 40
    TRUE = 41
    FALSE = 42
    KB = 43
    C = 44
    H = 45
    Q = 46

    # FUNCTIONS
    COS = 100
    ACOS = 101
    COSH = 102
    SIN = 103
    ASIN = 104
    SINH = 105
    TAN = 106
    ATAN = 107
    TANH = 108
    SQRT = 109
    EXP = 110
    LN = 111
    LOG = 112

    # CONVERSION
    DEG = 1000
    RAD = 1001
    LAST_FUNC = 1001

    # OTHER
    SAVE = 65532
    LOAD = 65533
    ANSWER = 65534
    EOF = 65535

    def __str__(self):
        return "TokenType." + self.name


keywords = {
    "pi": TokenType.PI,
    "kb": TokenType.KB,
    "h": TokenType.H,
    "c": TokenType.C,
    "q": TokenType.Q,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "ans": TokenType.ANSWER,
    "save": TokenType.SAVE,
    "load": TokenType.LOAD,
    "deg": TokenType.DEG,
    "rad": TokenType.RAD,

    "sep": TokenType.EOF,  # used for highlighter

    "exp": TokenType.EXP,
    "cos": TokenType.COS,
    "acos": TokenType.ACOS,
    "cosh": TokenType.COSH,
    "sin": TokenType.SIN,
    "asin": TokenType.ASIN,
    "sinh": TokenType.SINH,
    "tan": TokenType.TAN,
    "atan": TokenType.ATAN,
    "tanh": TokenType.TANH,
    "ln": TokenType.LN,
    "log": TokenType.LOG,
    "√": TokenType.SQRT,
    "sqrt": TokenType.SQRT
}


class Token:

    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.literal is None:
            lit = ""
        else:
            lit = self.literal.__str__()
        return self.type.__str__() + " " + self.lexeme + " " + lit
