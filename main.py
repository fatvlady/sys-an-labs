__author__ = 'vlad'
#coding: utf8
import sys

from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUiType

app = QApplication(sys.argv)
app.setApplicationName('lab2_sa')
form_class, base_class = loadUiType('main_window.ui')


class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        return


    def buttonClicked(self):
        sender = self.sender()
        QMessageBox.warning(self,'Hola!',sender.text())
        return

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        return


#-----------------------------------------------------#
form = MainWindow()
form.setWindowTitle('lab2_sa')
form.show()
sys.exit(app.exec_())