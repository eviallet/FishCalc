from PyQt5.QtWidgets import \
    QScrollArea,        \
    QTextEdit,          \
    QVBoxLayout,        \
    QWidget
from PyQt5.QtCore import pyqtSlot, Qt

from ui.style import get_style, SCROLL_AREA_STYLE
from ui.highlighter import Highlighter


HISTORY_ITEM_HEIGHT = 70


class History(QScrollArea):

    def __init__(self, parent):
        super(History, self).__init__(parent)
        self.count = 0

        widget = QWidget()
        font, style_sheet = get_style('QWidget')
        widget.setStyleSheet(style_sheet)
        self.setWidget(widget)
        self.vlayout = QVBoxLayout()
        widget.setLayout(self.vlayout)

        self.vlayout.setSpacing(0)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.verticalScrollBar().setStyleSheet(SCROLL_AREA_STYLE)
        self.verticalScrollBar().rangeChanged.connect(
            lambda: self.verticalScrollBar().setValue(
                self.verticalScrollBar().maximum()
            )
        )

        font, style_sheet = get_style('QScrollArea')
        self.setStyleSheet(style_sheet)

    @pyqtSlot(str)
    def put_history(self, query, ans):
        self.count += 1
        self.vlayout.addWidget(HistoryElement(query, ans), alignment=Qt.AlignTop)
        self.widget().setMaximumHeight(self.count * HISTORY_ITEM_HEIGHT)
        # TODO widgets go slightly away from each other when adding new items

    def last_query_bridge(self):
        def last_query(index):
            if self.count == 0 or self.count <= index:
                return None
            else:
                return self.vlayout.itemAt(self.count - 1 - index).widget().query
        return last_query


class HistoryElement(QTextEdit):

    def __init__(self, query, ans):
        super(HistoryElement, self).__init__()

        font, style_sheet = get_style('QTextEdit')
        self.setFont(font)
        self.setStyleSheet(style_sheet)

        self.query = query

        self.setReadOnly(True)
        self.setMinimumHeight(HISTORY_ITEM_HEIGHT)
        self.setMaximumHeight(HISTORY_ITEM_HEIGHT)
        html = Highlighter.highlight('<p>'+query+"<br>   → "+ans+'</p>')
        self.setHtml(html)

