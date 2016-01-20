#coding: utf8

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUiType
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


form_class, base_class = loadUiType('lab_4/graph_table.ui')


class DynamicRiskCanvas(FigureCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, parent=None, coordinate=1, dpi=100, real_size=50, warning=0, failure=0):
        self.coordinate = coordinate
        self.warning_threshold = warning
        self.failure_threshold = failure
        self.real_size = real_size
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title('$Y_{}$'.format(str(self.coordinate)), fontsize=10)
        self.real_line = self.axes.plot([], [], 'b')
        self.predicted_line = self.axes.plot([], [], 'g')
        self.risk_line = self.axes.plot([], [], 'g-')
        self.warning_line = self.axes.plot([], [], 'r-')
        self.failure_line = self.axes.plot([], [], 'r')
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(1000)

    def compute_initial_figure(self, real_values, predicted_values, risk_values, time_ticks):
        self.real_line.set_data(time_ticks[:self.real_size], real_values)
        self.predicted_line.set_data(time_ticks[self.real_size:], predicted_values)
        self.risk_line.set_data(time_ticks[self.real_size:], risk_values)
        self.warning_line.set_data(time_ticks, [self.warning_threshold] * len(time_ticks))
        self.failure_line.set_data(time_ticks, [self.failure_threshold] * len(time_ticks))
        self.draw()

    def update_figure(self, real_value, predicted_values, risk_values, time_ticks):
        l = [np.random.randint(0, 10) for i in range(4)]
        self.axes[0, 0].plot([0, 1, 2, 3], l, 'r')
        self.draw()


class OperatorViewWindow(QDialog):

    def __init__(self, *args, **kwargs):
        super(OperatorViewWindow, self).__init__(*args)
        warning = kwargs.get('warn', [0,0,0])
        failure = kwargs.get('fail', [0,0,0])
        real_size = kwargs.get('real_size', 50)
        self.ui = form_class()
        self.ui.setupUi(self)
        self.graphs = [DynamicRiskCanvas(self, coordinate=i + 1, warning=warning[i], failure=failure[i],
                                         real_size=real_size) for i in xrange(3)]
        for graph in self.graphs:
            self.ui.y_layout.addWidget(graph)

    def initial_graphics_fill(self):
        pass