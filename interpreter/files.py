from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFile
from interpreter.token import TokenType


class Files:

    def __init__(self, token):
        if token.type == TokenType.LOAD:
            self.exec = Files.load
        else:
            self.exec = Files.save

    @staticmethod
    def load():
        path = QFileDialog.getOpenFileName()
        file = QFile(path[0])
        if file.open(QFile.ReadOnly):
            content = str(file.readAll())[1:].replace("'", '').replace("\\r", '\r').replace("\\n", '\n')
            file.close()
            return content
        return None

    @staticmethod
    def save():
        return None
        # return QFileDialog.getSaveFileName()
