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
msg = QMessageBox()
msg.setWindowTitle("Movies2HDD")
sys.stdout.write("	Movies2HDD")
sys.stdout.flush()
import movies2hdd
Movies2HDD = movies2hdd.Movies2HDD()
sys.stdout.write("	...done.")
sys.stdout.flush()
sys.stdout.write("\n")
sys.stdout.flush()
print ("")


class Step1(QWizardPage):
	def __init__(self, parent=None):
		super(Step1, self).__init__(parent)
		self.setTitle("Select the folder and the series")
		self.layout = QVBoxLayout()
		self.introduction = QLabel("First, you need to select the folder where the movies are or should be placed. The name of the series is needed, too.")
		self.introduction.setWordWrap(True)
		self.layout.addWidget(self.introduction)
		self.form = QFormLayout()
		self.folder_selection = QPushButton("Select")
		self.folder_selection.clicked.connect(self.func_folder_selection)
		self.form.addRow(self.tr("Select &folder:"), self.folder_selection)
		self.series_selection = QPushButton("Select")
		self.series_selection.clicked.connect(self.func_series_selection)
		self.form.addRow(self.tr("Select &series:"), self.series_selection)
		self.layout.addLayout(self.form)
		self.setLayout(self.layout)

	def func_folder_selection(self):
		folder = QFileDialog.getExistingDirectory()
		self.folder_selection.setText(folder)

	def func_series_selection(self):
		seriesselection = SeriesSelection(self)
		seriesselection.setWindowModality(Qt.WindowModal)
		seriesselection.show()

	def validatePage(self):
		if self.folder_selection.text() != "Select" and self.series_selection != "Select":
			return(True)
		else:
			msg.setText("You need to select a folder and a series first.")
			msg.show()
			return(False)

class Step2(QWizardPage):
	def __init__(self, parent=None):
		super(Step2, self).__init__(parent)
		self.setTitle("Connect to your Dreambox")
		self.layout = QVBoxLayout()
		self.introduction = QLabel("")
		self.introduction.setWordWrap(True)
		self.setLayout(self.layout)


	def nextId(self):
		return(1)

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
			self.searchButton = QPushButton("Se&arch")
			self.layout.addWidget(self.searchButton)
			self.searchButton.clicked.connect(self.searchForSeries)

			self.table = QTableWidget()
			self.table.setColumnCount(3)
			self.table.setHorizontalHeaderLabels(["ID", "Series", "Overview"])
			self.layout.addWidget(self.table)

			self.button = QPushButton("Se&lect")
			self.layout.addWidget(self.button)
			self.button.clicked.connect(self.select)
			
			self.setLayout(self.layout)

		def searchForSeries(self):
			#progress = QProgressDialog("Searching for the series...", "Close", 0, 1, self)
			#progress.setWindowModality(Qt.WindowModal)
			#progress.setWindowTitle("Movies2HDD")
			#progress.setAutoClose(False)
			#progress.setCancelButton(None)
			#progress.setMinimumDuration(0)
			#progress.show()
			#progress.setValue(0)
			try:
				series = Movies2HDD.getSeries(self.form.series.text())
				#progress.setMaximum(series.__len__())
				self.table.clear()
				self.table.setRowCount(0)
				self.table.setHorizontalHeaderLabels(["ID", "Series", "Overview"])
				for x in series:
					#progress.setValue(progress.value() + 1)
					flags = int(Qt.ItemIsEnabled) #+ int(Qt.ItemIsSelectable)
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
			except:
				msg.setText("An error occured.")
				msg.show()
				#progress.hide()

		def select(self):
			item = self.table.item(self.table.currentRow(), 0)
			#The conversion str->int->str is not really needed. And it is nothing that the user can change. But it could prevent future issues.
			sid = int(item.text())
			self.parent().series_selection.setText(str(sid))
			self.close()
			

mainwindow = QWizard()
mainwindow.setWindowTitle("Movies2HDD")
mainwindow.step1 = Step1()
mainwindow.step2 = Step2()
mainwindow.addPage(mainwindow.step1)
mainwindow.addPage(mainwindow.step2)
mainwindow.show()
app.exec_()
try:
	Movies2HDD.disconnect()
except:
	pass
