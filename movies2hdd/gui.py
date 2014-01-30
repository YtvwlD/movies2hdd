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
print ("")

class MainWindow(PySide.QtGui.QDialog):

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
		self.layout = PySide.QtGui.QVBoxLayout()
		self.introduction = PySide.QtGui.QLabel("There are a few common tasks. These are listed below.\nIf you think that something is missing feel free to create an issue or a pull request.\nYou may want to take a look at the existing tasks.")
		self.layout.addWidget(self.introduction)
		self.commontasks = PySide.QtGui.QHBoxLayout()
		self.commontasks.downloadrenameconvert = PySide.QtGui.QPushButton("Download, rename and convert\n(You can choose which of them you want but the order is fixed.)")
		self.commontasks.addWidget(self.commontasks.downloadrenameconvert)
		self.commontasks.renameexisting = PySide.QtGui.QPushButton("Rename existing movies (needs the *.meta files)")
		self.commontasks.addWidget(self.commontasks.renameexisting)
		self.layout.addLayout(self.commontasks)
		self.setLayout(self.layout)

mainwindow = MainWindow()
mainwindow.show()
app.exec_()
Movies2HDD.disconnect()
