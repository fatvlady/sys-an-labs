#coding: utf8
import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType


form_class, base_class = loadUiType('lab_3/bruteforce_window.ui')


class BruteForceWindow(QDialog, form_class):
    update_degrees = pyqtSignal(int, int, int)

    def __init__(self, *args):
        super(BruteForceWindow, self).__init__(*args)

        self.setupUi(self)

    @staticmethod
    def launch(parent):
        dialog = BruteForceWindow(parent)
        dialog.update_degrees.connect(parent.update_degrees)
        dialog.setWindowTitle("Polynomial's degree finder")
        dialog.show()

    @pyqtSlot()
    def triggered(self):
        self.update_degrees.emit(3,3,3)
        return


