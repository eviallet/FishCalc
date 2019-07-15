from PyQt5.QtWidgets import QApplication
from ui.ui import MainWindow
from sys import argv

app = QApplication(argv)
window = MainWindow()
window.show()
exit(app.exec_())

