#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore, uic

class MyWindow(QtGui.QMainWindow):
	def __init__(self):    
		super(MyWindow, self).__init__()
		uic.loadUi('UIVis.ui', self)
		self.show()
		self.raise_() 

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())