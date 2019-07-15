from PyQt5.QtCore import pyqtSlot

from enum import Enum
from interpreter.token import keywords
import random


class Color(Enum):
    RED = '#b32424'
    ORANGE = '#cf660a'
    YELLOW = '#d4e024'
    LIME = '#8ddb2e'
    GREEN = '#389632'
    CYAN = '#0aa65d'
    BLUE = '#2a9da1'
    PINK = '#b51058'


COLORS = []
for col in Color:
    COLORS.append(col)
random.shuffle(COLORS)


class ReservedColors(Enum):
    # NUMBER = '#78eb9c'
    NUMBER = '#6897BB'
    IDENTIFIER = '#CC7832'
    FUNCTION = '#6A8759'
    KEYWORD = '#94558D'
    ERROR = '#F92672'


FUNCTIONS = []
KEYWORDS = []
keys = list(keywords.keys())

for j in range(0, len(keys)):
    if keys[j] != "sep":
        KEYWORDS.append(keys[j])
    else:
        j += 1
        while j < len(keys):
            FUNCTIONS.append(keys[j])
            j += 1
        break

ERRORS = ['MathError', 'ParseError', 'RuntimeError', 'ScanError']


class Html(Enum):
    COLOR_START = '<font color="'
    COLOR_MID = '">'
    COLOR_END = '</font>'


class Highlighter:

    deepness = 0

    @staticmethod
    @pyqtSlot(str)
    def highlight(text: str):
        Highlighter.deepness = 0

        i = 0
        while i < len(text):
            length = 1
            if text[i] == '(':
                text, length = Highlighter.colorize(text, i, i + 1, COLORS[Highlighter.deepness % len(COLORS)])
                Highlighter.deepness += 1
            elif text[i] == ')':
                Highlighter.deepness -= 1
                text, length = Highlighter.colorize(text, i, i + 1, COLORS[Highlighter.deepness % len(COLORS)])
            elif Highlighter.is_digit(text[i]):
                start_pos = i
                while i < len(text) and Highlighter.is_digit(text[i]):
                    i += 1
                if len(text) > i + 1 and text[i] == '.' and Highlighter.is_digit(text[i+1]):
                    i += 1
                elif len(text) > i + 1 and text[i] == 'e' and Highlighter.is_digit(text[i + 1]):
                    i += 1
                elif len(text) > i + 2 and text[i] == 'e' and (text[i+1] == '-' or text[i+1] == '+') and Highlighter.is_digit(text[i + 2]):
                    i += 2
                text, length = Highlighter.colorize(text, start_pos, i, ReservedColors.NUMBER)
            elif Highlighter.is_alpha(text[i]):
                start_pos = i
                i += 1
                while i < len(text) and Highlighter.is_alpha(text[i]):
                    i += 1
                sub_text = text[start_pos:i]
                if sub_text in FUNCTIONS:
                    text, length = Highlighter.colorize(text, start_pos, i, ReservedColors.FUNCTION)
                elif sub_text in KEYWORDS:
                    text, length = Highlighter.colorize(text, start_pos, i, ReservedColors.KEYWORD)
                elif sub_text in ERRORS:
                    text, length = Highlighter.colorize(text, start_pos, i, ReservedColors.ERROR)
                i -= 1

            i += length

        return text

    @staticmethod
    def colorize(text: str, start_pos: int, end_pos: int, color):
        new = text[:start_pos] + Html.COLOR_START.value + color.value + Html.COLOR_MID.value +\
               text[start_pos:end_pos] + Html.COLOR_END.value + text[end_pos:]
        return new, len(new) - len(text)

    @staticmethod
    def is_digit(c):
        return '0' <= c <= '9'

    @staticmethod
    def is_alpha(c):
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_' or c == '√'
