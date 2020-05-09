import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget

from ui_mainwindow import UI_MainWindow


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = UI_MainWindow()
    window.show()

    app.exec_()
1