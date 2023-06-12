# wburt 2023-06-12
# Example of pyqt5 with Gui

import sys
import socket
import os
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('get_server.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.pushButton.clicked.connect(self.get_server)
    def get_server(self):
        self.label.setText(socket.gethostname().upper())
    
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()