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
        self.cursor_pos = 0

        font, style_sheet = get_style('')

        self.setFont(font)
        self.setStyleSheet(TERMINAL_STYLE)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def keyPressEvent(self, key_event: QKeyEvent):
        if key_event.key() == Qt.Key_Left or key_event.key() == Qt.Key_Right:
            if key_event.key() == Qt.Key_Left: self.decrement_cursor_pos()
            if key_event.key() == Qt.Key_Right: self.increment_cursor_pos()
            super(Terminal, self).keyPressEvent(key_event)
            return

        self.setText(self.user_text)
        self.set_cursor_at_user_pos()

        if key_event.key() == Qt.Key_Up:
            self.history_up()
            key_event.accept()
        elif key_event.key() == Qt.Key_Down:
            self.history_down()
            key_event.accept()
        elif key_event.key() == Qt.Key_Enter or key_event.key() == Qt.Key_Return:
            self.interpret_request.emit(self.toPlainText())
            self.cursor_pos = 0
            self.clear_terminal()
        elif key_event.key() == Qt.Key_Space:
            # prevent successive spaces to break up the cursor (while translating to html)
            if len(self.toPlainText()) == 0 or self.toPlainText()[len(self.toPlainText()) - 1] != ' ':
                super(Terminal, self).keyPressEvent(key_event)
        elif key_event.key() == Qt.Key_Less:
            self.insertPlainText('&lt;')
            self.increment_cursor_pos(4)
        elif key_event.key() == Qt.Key_Greater:
            self.insertPlainText('&gt;')
            self.increment_cursor_pos(4)
        else:
            super(Terminal, self).keyPressEvent(key_event)

        # a character has been added to the text
        if len(self.user_text) - len(self.toPlainText().replace('<', '&lt;').replace('>', '&gt;')) == -1:
            self.increment_cursor_pos()
        # > 1 char added at the same time: pasted, history..
        elif len(self.user_text) - len(self.toPlainText().replace('<', '&lt;').replace('>', '&gt;')) < -1:
            self.set_cursor_at(QTextCursor.End)
        # a character has been removed
        elif len(self.user_text) - len(self.toPlainText().replace('<', '&lt;').replace('>', '&gt;')) == 1:
            self.decrement_cursor_pos()
        # multiple characters has been removed
        elif len(self.user_text) - len(self.toPlainText().replace('<', '&lt;').replace('>', '&gt;')) > 1:
            self.set_cursor_at(QTextCursor.Start)

        self.user_text = self.toPlainText()\
            .replace('sqrt', '√(').replace('->', '⇒')\
            .replace('<', '&lt;').replace('>', '&gt;')

        self.clear()
        self.insertHtml(Highlighter.highlight(self.user_text))
        self.set_cursor_at_user_pos()

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

    def increment_cursor_pos(self, inc=1):
        self.cursor_pos += inc

    def decrement_cursor_pos(self, dec=1):
        if not self.textCursor().atStart():
            self.cursor_pos -= dec

    def set_cursor_at_user_pos(self):
        cursor = self.textCursor()
        pos = self.cursor_pos
        if pos > len(self.toPlainText()):
            pos = len(self.toPlainText())
        cursor.setPosition(pos)
        self.setTextCursor(cursor)

    def set_cursor_at(self, pos):
        text_cursor = self.textCursor()
        text_cursor.movePosition(pos)
        self.setTextCursor(text_cursor)
        self.cursor_pos = text_cursor.position()

    def clear_terminal(self):
        self.clear()
        self.current_history_index = 0
