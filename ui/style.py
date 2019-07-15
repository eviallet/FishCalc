from PyQt5.QtGui import \
    QFontDatabase,      \
    QFont

def get_style(class_name, background_color='#272822'):
    # noinspection PyCallByClass,PyArgumentList
    font = QFont(
        QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont("res/fonts/SourceCodePro-Semibold.ttf")
        )[0]
    )
    font.setPointSize(12)

    style_sheet = """
            %s {
                background-color: %s;
                color: #F8F8F2;
                border: 0px;
            }
            """ % (class_name, background_color)

    return font, style_sheet


SCROLL_AREA_STYLE = """
            QScrollBar:vertical{
                background-color: #272822;
                width: 8px;
            }
            QScrollBar::handle:vertical{
                background-color: #3f403b;
                border-radius: 4px;
            }*
            QScrollBar::add-line:vertical{ height: 0px }
            QScrollBar::sub-line:vertical{ height: 0px }
            QScrollBar::add-page:vertical{ background: none }
            QScrollBar::sub-page:vertical{ background: none }
        """

TERMINAL_STYLE = """
            QTextEdit {
                background-color: #4b4e52;
                color: #F8F8F2;
                border: 0px;
                border-radius: 5px;
                padding: 4px;
            }
        """
