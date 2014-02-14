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

	def _makeBold(self, label):
		label.setText("<b>" + label.text() + "</b>")

	def _removeBold(self, label):
		label.setText(label.text()[3:-4])

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowTitle("Movies2HDD")
		self.layout = QHBoxLayout()
		#left
		self.left = QVBoxLayout()
		self.left.headline = QLabel("Movies2HDD")
		self._makeBold(self.left.headline)
		self.left.addWidget(self.left.headline)
		self.left.step1 = QLabel(" * Select folder and series")
		self._makeBold(self.left.step1)
		self.left.addWidget(self.left.step1)
		self.left.step2 =  QLabel("")
		self.left.addWidget(self.left.step2)
		#right
		self.right =  QVBoxLayout()
		#Step 1
		self.right.step1 =  QVBoxLayout()
		self.right.step1.headline = QLabel("<b>Select the folder and the series</b>")
		self.right.step1.addWidget(self.right.step1.headline)
		self.right.step1.introduction = QLabel("First, you need to select the folder where the movies are or should be placed. The name of the series is needed, too.")
		self.right.step1.introduction.setWordWrap(True)
		self.right.step1.addWidget(self.right.step1.introduction)
		self.right.step1.form = QFormLayout()
		self.right.step1.folder_selection = QPushButton("Select")
		self.right.step1.folder_selection.clicked.connect(self.func_step1_folder_selection)
		self.right.step1.form.addRow(self.tr("Select &folder:"), self.right.step1.folder_selection)
		self.right.step1.series_selection = QPushButton("Select")
		self.right.step1.series_selection.clicked.connect(self.func_step1_series_selection)
		self.right.step1.form.addRow(self.tr("Select &series:"), self.right.step1.series_selection)
		self.right.step1.addLayout(self.right.step1.form)
		#TODO Connect the buttons to some functions


		#self.right.step1.host = ""QLineEdit()
		#self.right.step1.host.layout =  QHBoxLayout()
		#self.right.step1.host.label =  QLabel("Host: ")
		#self.right.step1.host.layout.addWidget(self.right.step1.host.label)
		#self.right.step1.host.layout.addWidget(self.right.step1.host)
		#self.right.step1.addLayout(self.right.step1.host.layout)
		#self.right.step1.user =  QLineEdit()
		#self.right.step1.user.layout =  QHBoxLayout()
		#self.right.step1.user.label =  QLabel("User: ")
		#self.right.step1.user.layout.addWidget(self.right.step1.user.label)
		#self.right.step1.user.layout.addWidget(self.right.step1.user)
		#self.right.step1.addLayout(self.right.step1.user.layout)
		#self.right.step1.pwd =  QLineEdit()
		#self.right.step1.pwd.layout =  QHBoxLayout()
		#self.right.step1.pwd.label =  QLabel("Password: ")
		#self.right.step1.pwd.layout.addWidget(self.right.step1.pwd.label)
		#self.right.step1.pwd.layout.addWidget(self.right.step1.pwd)
		#self.right.step1.addLayout(self.right.step1.pwd.layout)
		#self.right.step1.button =  QPushButton("Connect")
		#self.right.step1.addWidget(self.right.step1.button)
		#self.right.step1.button.clicked.connect(self.connecttodream)
		#self.right.step2 =  QVBoxLayout()
		#self.right.step2.headline =  QLabel("2 Search for movies")
		#self.right.step2.addWidget(self.right.step2.headline)
		#self.right.step2.search =  QLineEdit()
		#self.right.step2.search.layout =  QHBoxLayout()
		#self.right.step2.search.label =  QLabel("Search for: ")
		#self.right.step2.search.layout.addWidget(self.right.step2.search.label)
		#self.right.step2.search.layout.addWidget(self.right.step2.search)
		#self.right.step2.search.button =  QPushButton("Search")
		#self.right.step2.search.layout.addWidget(self.right.step2.search.button)
		#self.right.step2.addLayout(self.right.step2.search.layout)
		#...
		self.right.addLayout(self.right.step1)
		self._showLayout(self.right.step1)
		#self._hideLayout(self.right.step2)
		#self.right.addLayout(self.right.step2)
		self.right.buttons = QHBoxLayout()
		self.right.buttons.cancel = QPushButton("&Cancel")
		self.right.buttons.cancel.layout = QHBoxLayout()
		self.right.buttons.cancel.layout.setAlignment(Qt.AlignLeft)
		self.right.buttons.cancel.layout.addWidget(self.right.buttons.cancel)
		self.right.buttons.addLayout(self.right.buttons.cancel.layout)
		self.right.buttons.backandnext = QHBoxLayout()
		self.right.buttons.backandnext.setAlignment(Qt.AlignRight)
		self.right.buttons.backandnext.back = QPushButton("&Back")
		self.right.buttons.backandnext.addWidget(self.right.buttons.backandnext.back)
		self.right.buttons.backandnext.next = QPushButton("&Next")
		self.right.buttons.backandnext.addWidget(self.right.buttons.backandnext.next)
		self.right.buttons.addLayout(self.right.buttons.backandnext)
		self.right.addLayout(self.right.buttons)
		self.layout.addLayout(self.left)
		self.layout.addLayout(self.right)
		self.setLayout(self.layout)

	def func_step1_folder_selection(self):
		folder = QFileDialog.getExistingDirectory()
		self.right.step1.folder_selection.setText(folder)

	def func_step1_series_selection(self):
		seriesselection = SeriesSelection(self)
		seriesselection.show()

class SeriesSelection(QDialog):
		def __init__(self, parent):
			super(SeriesSelection, self).__init__(parent)
			self.setWindowTitle("Series Selection")
			self.layout = QVBoxLayout()
			self.introduction = QLabel("Please enter the name of the series to search for and the language code.")
			self.introduction.setWordWrap(True)
			self.layout.addWidget(self.introduction)
			self.form = QFormLayout()
			self.form.series = QLineEdit()
			self.form.addRow(self.tr("&Series:"), self.form.series)
			self.form.lang = QLineEdit()
			self.form.addRow(self.tr("&Language code:"), self.form.lang)
			self.layout.addLayout(self.form)
			self.searchButton = QPushButton("&Search")
			self.layout.addWidget(self.searchButton)
			self.searchButton.clicked.connect(self.searchForSeries)

			self.table = QTableWidget()
			self.table.setColumnCount(3)
			self.table.setHorizontalHeaderLabels(["ID", "Series", "Overview"])
			self.layout.addWidget(self.table)
			
			self.setLayout(self.layout)

		def searchForSeries(self):
			series = Movies2HDD.getSeries(self.form.series.text())
			self.table.clear()
			self.table.setRowCount(0)
			self.table.setHorizontalHeaderLabels(["ID", "Series", "Overview"])
			for x in series:
				flags = int(Qt.ItemIsEnabled) + int(Qt.ItemIsSelectable)
				self.table.setRowCount(self.table.rowCount() + 1)
				sidItem = QTableWidgetItem(x['seriesid'])
				sidItem.setFlags(flags)
				self.table.setItem(self.table.rowCount() - 1, 0, sidItem)
				SeriesNameItem = QTableWidgetItem(x['SeriesName'])
				SeriesNameItem.setFlags(flags)
				self.table.setItem(self.table.rowCount() - 1, 1, SeriesNameItem)
				OverviewItem = QTableWidgetItem(x['Overview'].replace("\n", "   "))
				OverviewItem.setFlags(flags)
				self.table.setItem(self.table.rowCount() - 1, 2, OverviewItem)
			

mainwindow = MainWindow()
mainwindow.show()
app.exec_()
try:
	Movies2HDD.disconnect()
except:
	pass
