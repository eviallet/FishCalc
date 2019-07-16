from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent, QTextCursor
from ui.style import get_style, TERMINAL_STYLE
from ui.highlighter import Highlighter


class Terminal(QTextEdit):

    interpret_request = pyqtSignal(str)

    def __init__(self, last_query_bridge, other=None):
        super(Terminal, self).__init__(other)

        self.cmd = ''
        self.history = []
        self.last_query = last_query_bridge
        self.current_history_index = 0
        self.user_text = ''
        self.user_text = ''

        font, style_sheet = get_style('')

        self.setFont(font)
        self.setStyleSheet(TERMINAL_STYLE)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # TODO move cursor can edit text
    def keyPressEvent(self, key_event: QKeyEvent):
        if key_event.key() == Qt.Key_Left or key_event.key() == Qt.Key_Right:
            super(Terminal, self).keyPressEvent(key_event)
            return

        self.setText(self.user_text)
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

        if key_event.key() == Qt.Key_Up:
            self.history_up()
            key_event.accept()
        elif key_event.key() == Qt.Key_Down:
            self.history_down()
            key_event.accept()
        elif key_event.key() == Qt.Key_Enter or key_event.key() == Qt.Key_Return:
            self.interpret_request.emit(self.toPlainText())
            self.clear_terminal()
        elif key_event.key() == Qt.Key_Less:
            self.insertPlainText('&lt;')
        elif key_event.key() == Qt.Key_Greater:
            self.insertPlainText('&gt;')
        else:
            super(Terminal, self).keyPressEvent(key_event)

        self.user_text = self.toPlainText()\
            .replace('sqrt', '√(').replace('->', '⇒')\
            .replace('<', '&lt;').replace('>', '&gt;')

        self.clear()
        self.insertHtml(Highlighter.highlight(self.user_text))

    def history_up(self):
        query = self.last_query(self.current_history_index)
        if query is not None:
            self.setText(query)
            self.current_history_index += 1
            if self.last_query(self.current_history_index) is None:
                self.current_history_index -= 1

    def history_down(self):
        if not self.current_history_index == 0:
            self.current_history_index -= 1
            query = self.last_query(self.current_history_index)
            if query is not None:
                self.setText(query)
                if self.current_history_index < 0:
                    self.current_history_index = 0
            else:
                self.clear_terminal()
        else:
            self.clear_terminal()

    def clear_terminal(self):
        self.clear()
        self.current_history_index = 0
