from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from sympy.parsing import sympy_parser as parser
from sympy import init_printing
from sympy import latex


init_printing()


class Renderer(QHBoxLayout):

    def __init__(self, parent=None):
        super(QHBoxLayout, self).__init__(parent)

        self.fig = Figure()

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.resize(500, 260)
        self.addWidget(self.canvas)

        self.fig.suptitle('$x=\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}$',
                          x=0.0, y=0.5,
                          horizontalalignment='left',
                          verticalalignment='center')
        self.canvas.draw()

    @pyqtSlot(str)
    def render(self, text):
        print("=== rendering : %s" % text)

        expr = parser.parse_expr(text, evaluate=False)
        expr = "$" + latex(expr) + "$"

        print("-> result is : %s" % expr)

        self.fig.suptitle(expr,
                          x=0.0, y=0.5,
                          horizontalalignment='left',
                          verticalalignment='center')
        self.canvas.draw()

