#coding: utf8
import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType
from lab_3.Calculate_optimal_degrees import *

form_class, base_class = loadUiType('lab_3/bruteforce_window.ui')


class BruteForceWindow(QDialog, form_class):
    update_degrees = pyqtSignal(int, int, int)

    def __init__(self, *args):
        super(BruteForceWindow, self).__init__(*args)
        self.setupUi(self)

    @staticmethod
    def launch(parent):
        dialog = BruteForceWindow(parent)
        dialog.params = parent._get_params()
        dialog.update_degrees.connect(parent.update_degrees)
        dialog.setWindowTitle("Polynomial's degree finder")
        dialog.show()

    @pyqtSlot()
    def triggered(self):
        self.low_edge  = [self.from_1.value(), self.from_2.value(), self.from_3.value()]
        self.high_edge = [self.to_1.value(), self.to_2.value(), self.to_3.value()]
        self.step = [self.st_1.value(), self.st_2.value(), self.st_3.value()]
        solver = Solve(self.params)
        p = [[i for i in range(self.low_edge[j], self.high_edge[j]+1, self.step[j])] for j in range(len(self.step))]
        x1_deg, x2_deg, x3_deg = determine_deg(solver, p[0], p[1], p[2])
        self.res_1.setValue(x1_deg)
        self.res_2.setValue(x2_deg)
        self.res_3.setValue(x3_deg)
        #self.update_degrees.emit(3,3,3)
        return

    def _process_bruteforce(self, lower, upper):
        pass

