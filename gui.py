#!/usr/bin/env python3
'''A GUI to Movies2HDD.'''




if __name__ == "__main__":
	import sys
	sys.stdout.write("Loading...")
	sys.stdout.flush()
	sys.stdout.write("	PySide")
	sys.stdout.flush()
	import PySide
	import PySide.QtCore
	import PySide.QtGui
	app = PySide.QtGui.QApplication(sys.argv)
	sys.stdout.write("	Movies2HDD")
	sys.stdout.flush()
	import movies2hdd
	Movies2HDD = movies2hdd.Movies2HDD()
	sys.stdout.write("	...done.")
	sys.stdout.flush()
	sys.stdout.write("\n")
	sys.stdout.flush()

class MainWindow(PySide.QtGui.QDialog):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("Movies2HDD")
		self.layout = PySide.QtGui.QHBoxLayout()
		#right
		self.right = PySide.QtGui.QVBoxLayout()
		self.right.headline = PySide.QtGui.QLabel("Movies2HDD")
		self.right.addWidget(self.right.headline)
		self.right.step1 = PySide.QtGui.QLabel("1. Connect to your DreamBox")
		self.right.addWidget(self.right.step1)
		#left
		self.left = PySide.QtGui.QHBoxLayout()
		#Step 1
		self.left.step1 = PySide.QtGui.QVBoxLayout()
		self.left.step1.headline = PySide.QtGui.QLabel("1. Connect to your DreamBox")		
		self.left.step1.addWidget(self.left.step1.headline)
		self.left.step1.host = PySide.QtGui.QLineEdit()
		self.left.step1.host.layout = PySide.QtGui.QHBoxLayout()
		self.left.step1.host.label = PySide.QtGui.QLabel("Host: ")
		self.left.step1.host.layout.addWidget(self.left.step1.host.label)
		self.left.step1.host.layout.addWidget(self.left.step1.host)
		self.left.step1.addLayout(self.left.step1.host.layout)
		self.left.step1.user = PySide.QtGui.QLineEdit()
		self.left.step1.user.layout = PySide.QtGui.QHBoxLayout()
		self.left.step1.user.label = PySide.QtGui.QLabel("User: ")
		self.left.step1.user.layout.addWidget(self.left.step1.user.label)
		self.left.step1.user.layout.addWidget(self.left.step1.user)
		self.left.step1.addLayout(self.left.step1.user.layout)
		self.left.step1.pwd = PySide.QtGui.QLineEdit()
		self.left.step1.pwd.layout = PySide.QtGui.QHBoxLayout()
		self.left.step1.pwd.label = PySide.QtGui.QLabel("Password: ")
		self.left.step1.pwd.layout.addWidget(self.left.step1.pwd.label)
		self.left.step1.pwd.layout.addWidget(self.left.step1.pwd)
		self.left.step1.addLayout(self.left.step1.pwd.layout)
		self.left.step1.button = PySide.QtGui.QPushButton("Connect")
		self.left.step1.addWidget(self.left.step1.button)
		#...
		self.left.addLayout(self.left.step1)
		self.layout.addLayout(self.left)
		self.layout.addLayout(self.right)
		self.setLayout(self.layout)

mainwindow = MainWindow()
mainwindow.show()
app.exec_()
