from PyQt5.QtWidgets import \
    QMainWindow,    \
    QVBoxLayout,    \
    QWidget

from PyQt5.QtGui import \
    QIcon

from PyQt5.QtCore import \
    pyqtSlot,       \
    QSize,          \
    Qt

import ctypes
from interpreter.interpreter import Interpreter
from ui.terminal import Terminal
from ui.history import History
from ui.style import get_style


WIDTH = 600
HEIGHT = 400


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.interpreter = Interpreter()

        self.history = History(self)
        self.terminal = Terminal(self.history.last_query_bridge())

        # noinspection PyUnresolvedReferences
        self.terminal.interpret_request.connect(self.interpreter.interpret)
        self.interpreter.interpreted.connect(self.on_interpreted)

        self.setup_ui()

    def setup_ui(self):
        # MainWindow
        self.setWindowTitle("FishCalc")
        self.setWindowIcon(QIcon("res/calculator.ico"))
        self.setFixedSize(QSize(WIDTH, HEIGHT))

        # taskbar icon
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.gueg.fishcalc')

        font, style_sheet = get_style('QMainWindow')

        self.setStyleSheet(style_sheet)

        # Central widget
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.history, alignment=Qt.AlignCenter)
        layout.addWidget(self.terminal, alignment=Qt.AlignCenter)
        self.history.setFixedSize(QSize(WIDTH-20, HEIGHT-50))
        self.terminal.setFixedSize(QSize(WIDTH-20, 30))
        self.setCentralWidget(widget)

        self.terminal.setFocus()

    @pyqtSlot(str)
    def on_interpreted(self, ans):
        self.history.put_history(self.terminal.user_text, ans)

