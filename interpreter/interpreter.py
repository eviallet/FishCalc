from PyQt5.QtCore import QObject, pyqtSignal
from interpreter.scanner import Scanner
from interpreter.parser import Parser
from interpreter.expr import Expr
from interpreter.errors import Error
from interpreter.files import Files


class Interpreter(QObject):

    interpreted = pyqtSignal(str)

    def __init__(self):
        super(Interpreter, self).__init__()
        self.scanner = Scanner()
        self.parser = Parser()
        self.was_retry = False

    def interpret(self, text: str):
        try:
            tokens, had_error = self.scanner.scan(text)
        except Error as err:
            self.print(err.__str__())
            return
        # for token in tokens: print(token)
        exprs = self.parser.parse(tokens)
        if exprs is not None:
            for expr in exprs:
                if isinstance(expr, Expr):
                    # print(expr.__str__())
                    try:
                        ans = expr.evaluate()
                        # TODO loaded script compatible with 'ans'
                        self.parser.environment.vars['ans'] = ans
                        if type(ans) is bool and not expr.mute:
                            if ans is True:
                                self.print("true")
                            else:
                                self.print("false")
                        else:
                            trimmed = self.trim_trailing_zero(ans)
                            if not expr.mute:
                                self.print(trimmed)
                    except Error as err:
                        self.print(err.__str__())
                elif isinstance(expr, Error):
                    print(expr.__str__())
                    # flexibility about unmatched ')' : allow "a = log(10" by adding a ')' at the end of the text
                    if (expr.__str__() == "ParseError - Expect ')' after arguments."
                        or expr.__str__() == "ParseError - Expect ')' after expression.") \
                            and not self.was_retry:
                        try:
                            self.was_retry = True
                            self.interpret(text + ')')
                        except Error:
                            self.print(expr)
                    else:
                        self.print(expr)
                elif isinstance(expr, Files):
                    loaded = expr.exec()
                    if loaded is not None:
                        self.interpret(loaded)
                        # TODO correct history for loaded scripts
        self.was_retry = False

    def print(self, res):
        self.interpreted.emit(res.__str__())
        # print(res)

    @staticmethod
    def trim_trailing_zero(text):
        text = str(text)
        if text.endswith('.0'):
            text = text[:text.index('.0')]
        return text
