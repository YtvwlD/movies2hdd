#!/usr/bin/env python3
'''A GUI to Movies2HDD.'''

#	Copyright (C) 2013 Niklas Sombert
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

print ("Movies2HDD's graphical user interface Copyright (C) 2013 Niklas Sombert")
print ("This program comes with ABSOLUTELY NO WARRANTY.")
print ("This is free software, and you are welcome to redistribute it")
print ("under certain conditions.")

print ("")

import sys
sys.stdout.write("Loading...")
sys.stdout.flush()
sys.stdout.write("	PySide")
sys.stdout.flush()
from PySide.QtCore import *
from PySide.QtGui import *
app =  QApplication(sys.argv)
sys.stdout.write("	Movies2HDD")
sys.stdout.flush()
import movies2hdd
Movies2HDD = movies2hdd.Movies2HDD()
sys.stdout.write("	...done.")
sys.stdout.flush()
sys.stdout.write("\n")
sys.stdout.flush()
print ("")

class MainWindow(QDialog):

	def _hideLayout(self, layout):
		for i in range(layout.count()):
			x = layout.itemAt(i)
			if x.widget() != None:
				x.widget().hide()
			else:
				self._hideLayout(x)

	def _showLayout(self, layout):
		for i in range(layout.count()):
			x = layout.itemAt(i)
			if x.widget() != None:
				x.widget().show()
			else:
				self._showLayout(x)

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("Movies2HDD")
		self.layout = QHBoxLayout()
		#right
		self.right = QVBoxLayout()
		self.right.headline = QLabel("Movies2HDD")
		self.right.addWidget(self.right.headline)
		self.right.step1 = QLabel("1 Select the folder and series")
		self.right.addWidget(self.right.step1)
		self.right.step2 =  QLabel("2 ")
		self.right.addWidget(self.right.step2)
		#left
		self.left =  QVBoxLayout()
		#Step 1
		self.left.step1 =  QVBoxLayout()
		self.left.step1.headline = QLabel("1 Select the folder and the series")
		self.left.step1.addWidget(self.left.step1.headline)
		self.left.step1.introduction = QLabel("First, you need to select the folder where the movies are or should be placed.\nThe name of the series is needed, too.")
		self.left.step1.addWidget(self.left.step1.introduction)
		self.left.step1.form = QFormLayout()
		self.left.step1.folder_selection = QPushButton("Select")
		#self.left.step1.folder_selection.description = QLabel("Select folder")
		self.left.step1.form.addRow(self.tr("Select &folder:"), self.left.step1.folder_selection)
		self.left.step1.series_selection = QPushButton("Select")
		self.left.step1.form.addRow(self.tr("Select &series:"), self.left.step1.series_selection)
		self.left.step1.addLayout(self.left.step1.form)
		#TODO Connect the buttons to some functions


		#self.left.step1.host = ""QLineEdit()
		#self.left.step1.host.layout =  QHBoxLayout()
		#self.left.step1.host.label =  QLabel("Host: ")
		#self.left.step1.host.layout.addWidget(self.left.step1.host.label)
		#self.left.step1.host.layout.addWidget(self.left.step1.host)
		#self.left.step1.addLayout(self.left.step1.host.layout)
		#self.left.step1.user =  QLineEdit()
		#self.left.step1.user.layout =  QHBoxLayout()
		#self.left.step1.user.label =  QLabel("User: ")
		#self.left.step1.user.layout.addWidget(self.left.step1.user.label)
		#self.left.step1.user.layout.addWidget(self.left.step1.user)
		#self.left.step1.addLayout(self.left.step1.user.layout)
		#self.left.step1.pwd =  QLineEdit()
		#self.left.step1.pwd.layout =  QHBoxLayout()
		#self.left.step1.pwd.label =  QLabel("Password: ")
		#self.left.step1.pwd.layout.addWidget(self.left.step1.pwd.label)
		#self.left.step1.pwd.layout.addWidget(self.left.step1.pwd)
		#self.left.step1.addLayout(self.left.step1.pwd.layout)
		#self.left.step1.button =  QPushButton("Connect")
		#self.left.step1.addWidget(self.left.step1.button)
		#self.left.step1.button.clicked.connect(self.connecttodream)
		#self.left.step2 =  QVBoxLayout()
		#self.left.step2.headline =  QLabel("2 Search for movies")
		#self.left.step2.addWidget(self.left.step2.headline)
		#self.left.step2.search =  QLineEdit()
		#self.left.step2.search.layout =  QHBoxLayout()
		#self.left.step2.search.label =  QLabel("Search for: ")
		#self.left.step2.search.layout.addWidget(self.left.step2.search.label)
		#self.left.step2.search.layout.addWidget(self.left.step2.search)
		#self.left.step2.search.button =  QPushButton("Search")
		#self.left.step2.search.layout.addWidget(self.left.step2.search.button)
		#self.left.step2.addLayout(self.left.step2.search.layout)
		#...
		self.left.addLayout(self.left.step1)
		self._showLayout(self.left.step1)
		#self._hideLayout(self.left.step2)
		#self.left.addLayout(self.left.step2)
		self.left.buttons = QHBoxLayout()
		self.left.buttons.cancel = QPushButton("Cancel")
		self.left.buttons.cancel.layout = QHBoxLayout()
		self.left.buttons.cancel.layout.setAlignment(Qt.AlignLeft)
		self.left.buttons.cancel.layout.addWidget(self.left.buttons.cancel)
		self.left.buttons.addLayout(self.left.buttons.cancel.layout)
		self.left.buttons.backandnext = QHBoxLayout()
		self.left.buttons.backandnext.setAlignment(Qt.AlignRight)
		self.left.buttons.backandnext.back = QPushButton("Back")
		self.left.buttons.backandnext.addWidget(self.left.buttons.backandnext.back)
		self.left.buttons.backandnext.next = QPushButton("Next")
		self.left.buttons.backandnext.addWidget(self.left.buttons.backandnext.next)
		self.left.buttons.addLayout(self.left.buttons.backandnext)
		self.left.addLayout(self.left.buttons)
		self.layout.addLayout(self.left)
		self.layout.addLayout(self.right)
		self.setLayout(self.layout)


mainwindow = MainWindow()
mainwindow.show()
app.exec_()
try:
	Movies2HDD.disconnect()
except:
	pass
