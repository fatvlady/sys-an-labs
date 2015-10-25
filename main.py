__author__ = 'vlad'
# coding: utf8

import sys
import numpy as np

from PyQt5.QtCore import pyqtSlot,pyqtSignal,Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUiType

app = QApplication(sys.argv)
app.setApplicationName('lab2_sa')
form_class, base_class = loadUiType('main_window.ui')


class MainWindow(QDialog, form_class):

    # signals:
    input_changed = pyqtSignal('QString')
    output_changed = pyqtSignal('QString')
    # x1_dim_changed = pyqtSignal(int)
    # x2_dim_changed = pyqtSignal(int)
    # x3_dim_changed = pyqtSignal(int)
    # x1_deg_changed = pyqtSignal(int)
    # x2_deg_changed = pyqtSignal(int)
    # x3_deg_changed = pyqtSignal(int)
    # type_cheb = pyqtSignal()
    # type_lege = pyqtSignal()
    # type_lagg = pyqtSignal()
    # type_herm = pyqtSignal()


    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)

        # setting up ui
        self.setupUi(self)

        # other initializations
        self.dimensions = np.array([self.x1_dim.value, self.x2_dim.value,
                                    self.x3_dim.value, self.y_dim.value])
        self.degrees = np.array([self.x1_deg.value, self.x2_deg.value, self.x3_deg.value])
        self.type = 'null'
        if self.radio_cheb.isChecked():
            self.type = 'chebyshev'
        elif self.radio_legend.isChecked():
            self.type = 'legendre'
        elif self.radio_lagg.isChecked():
            self.type = 'lagger'
        elif self.radio_herm.isChecked():
            self.type = 'hermit'
        self.input_path = ''
        self.output_path = ''
        return

    @pyqtSlot()
    def input_clicked(self):
        filename = QFileDialog.getOpenFileName(self,'Open data file','.', 'Data file (*.txt *.dat)')[0]
        if filename == '':
            return
        if filename != self.input_path:
            self.input_path = filename
            self.input_changed.emit(filename)
        print(filename)
        return

    @pyqtSlot('QString')
    def input_modified(self, value):
        print('new input: ' + value)
        return

    @pyqtSlot()
    def output_clicked(self):
        print('output clicked')
        return

    @pyqtSlot('QString')
    def output_modified(self, value):
        print('new output: ' + value)
        return

    @pyqtSlot(int)
    def samples_modified(self, value):
        print('samples modified:' + value)
        return

    @pyqtSlot(int)
    def dimension_modified(self, value):
        print('dimension modified:' + self.sender().text())
        return

    @pyqtSlot(int)
    def degree_modified(self, value):
        print('degree modified:' + self.sender().text())
        return

    @pyqtSlot(bool)
    def type_modified(self, isdown):
        print('type: ' + self.sender().text() + ' ' + str(isdown))
        return

    @pyqtSlot()
    def plot_clicked(self):
        print('plot clicked')
        return

    @pyqtSlot()
    def exec_clicked(self):
        print('exec clicked')
        return




#-----------------------------------------------------#
form = MainWindow()
form.setWindowTitle('System Analysis - Lab 2')
form.show()
sys.exit(app.exec_())