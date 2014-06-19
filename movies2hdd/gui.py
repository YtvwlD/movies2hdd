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
from PySide.QtCore import Qt
from PySide.QtGui import QDialog, QApplication, QMessageBox, QWizardPage, QWizard, QVBoxLayout, QLabel, QFormLayout, QPushButton, QLineEdit, QCheckBox, QGroupBox, QListWidget, QAbstractItemView, QFileDialog, QTableWidget, QTableWidgetItem, QListWidget
app =  QApplication(sys.argv)
msg = QMessageBox()
msg.setWindowTitle("Movies2HDD")
sys.stdout.write("	Movies2HDD")
sys.stdout.flush()
from movies2hdd import Movies2HDD
movies2hdd = Movies2HDD()
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
		self.registerField("folder_selection", self.folder_selection)
		self.folder_selection.clicked.connect(self.func_folder_selection)
		self.form.addRow(self.tr("Select &folder:"), self.folder_selection)
		self.series_selection = QPushButton("Select")
		self.registerField("seriesid", self.series_selection)
		self.series_selection.clicked.connect(self.func_series_selection)
		self.form.addRow(self.tr("Select &series:"), self.series_selection)
		self.layout.addLayout(self.form)
		self.setLayout(self.layout)

		self.lang = QLineEdit()
		self.registerField("lang", self.lang)


	def func_folder_selection(self):
		folder = QFileDialog.getExistingDirectory()
		self.folder_selection.setText(folder)
		self.setField("folder_selection", folder)

	def func_series_selection(self):
		seriesselection = SeriesSelection(self)
		seriesselection.setWindowModality(Qt.WindowModal)
		seriesselection.show()

	def validatePage(self):
		if self.folder_selection.text() != "Select" and self.series_selection != "Select" and self.folder_selection.text() != "":
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
		#self.introduction = QLabel("")
		#self.introduction.setWordWrap(True)
		#self.layout.addWidget(self.introduction)
		self.check = QCheckBox("Do the movies need to be &downloaded?")
		self.check.stateChanged.connect(self.func_check)
		self.layout.addWidget(self.check)

		self.group = QGroupBox("Connection information")
		self.group.layout = QVBoxLayout()
		self.group.form = QFormLayout()

		self.host = QLineEdit()
		self.registerField("host", self.host)
		self.group.form.addRow(self.tr("&Host:"), self.host)
		self.user = QLineEdit()
		self.registerField("user", self.user)
		self.group.form.addRow(self.tr("&User:"), self.user)
		self.warning = QLabel("<strong color='red'>Warning:</strong> Your password will be sent unencryptedly!\nPlease do this only if you trust the network that you are currently connected to.\nOtherwise please tunnel your connection for example via SSH or VPN.")
		self.warning.setWordWrap(True)
		self.group.form.addRow(self.warning)
		self.password = QLineEdit()
		self.registerField("password", self.password)
		self.password.setEchoMode(QLineEdit.EchoMode.Password)
		self.group.form.addRow(self.tr("&Password:"), self.password)

		self.group.layout.addLayout(self.group.form)
		self.group.setLayout (self.group.layout)
		self.layout.addWidget(self.group)
		self.group.setEnabled(False)

		self.setLayout(self.layout)

	def func_check(self):
		self.group.setEnabled(self.check.isChecked())


	def validatePage(self):
		if self.check.isChecked() == False:
			return(True)
		else:
			try:
				movies2hdd.connect(self.host.text(), self.user.text(), self.password.text())
				return(True)
			except Exception as e:
				#sys.stderr.write("ERROR: " + str(e) + "\n")
				msg.setText("Could not connect.\nPlease check your input and your connection.\n\nThe detailed error message is:\n"+str(e))
				msg.show()
				raise
				return(False)

	def nextId(self):
		if self.check.isChecked() == False:
			return(3)
		else:
			return(2)

class Step3(QWizardPage):
	def __init__(self, parent=None):
		super(Step3, self).__init__(parent)
		self.setTitle("Search for and select movies")
		self.layout = QVBoxLayout()
		self.introduction = QLabel("Please enter a string to search for:")
		self.introduction.setWordWrap(True)
		self.layout.addWidget(self.introduction)
		self.form = QFormLayout()
		self.lineEdit = QLineEdit()
		self.form.addRow(self.tr("&Search string:"), self.lineEdit)
		self.layout.addLayout(self.form)
		self.pushButton = QPushButton("S&earch")
		self.pushButton.clicked.connect(self.func_search)
		self.layout.addWidget(self.pushButton)
		self.list = QListWidget()
		self.list.setSelectionMode(QAbstractItemView.MultiSelection)
		self.layout.addWidget(self.list)
		self.setLayout(self.layout)

	def func_search(self):
		self.list.clear()
		movies = []
		try:
			movies = movies2hdd.getAviableMovies(str(self.lineEdit.text()))
		except:
			try:
				movies2hdd.connect(self.field("host"), self.field("user"), self.field("password"))
				movies = movies2hdd.getAviableMovies(str(self.lineEdit.text()))
			except Exception as e:
				#sys.stderr.write("ERROR: " + str(e)+ "\n")
				msg.setText("Something went wrong.\n\nThe detailed error message is:\n"+str(e))
				msg.show()
				raise
		finally:
			for x in movies:
				self.list.addItem(QListWidgetItem(x))
			

	def validatePage(self):
		if self.list.count() == 0:
			msg.setText("Didn't you want to search for movies?")
			msg.show()
			return(False)
		selectedMovies = self.list.selectedItems()
		if selectedMovies.__len__() == 0:
			msg.setText("Don't you want to select any items?")
			msg.show()
			return(False)
		self.parent().moviesSelectedForDownload = selectedMovies
		return(True)

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
				series = movies2hdd.getSeries(self.form.series.text())
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
			except Exception as e:
				#sys.stderr.write("ERROR: " + str(e)+ "\n")
				msg.setText("An error occured.\n\nThe detailed error message is:\n"+str(e))
				msg.show()
				#progress.hide()
				raise


		def select(self):
			if(self.form.lang.text()!= ""):
				try:
					item = self.table.item(self.table.currentRow(), 0)
					#The conversion str->int->str is not really needed. And it is nothing that the user can change. But it could prevent future issues.
					sid = str(int(item.text()))
					self.parent().series_selection.setText(sid)
					self.parent().setField("seriesid", sid)
					self.parent().setField("lang", self.form.lang.text())
					self.close()
				except:
					msg.setText("You need to select one series by clicking on it.")
					msg.show()
			else:
				msg.setText("You need to enter your language code.")
				msg.show()


mainwindow = QWizard()
mainwindow.setWindowTitle("Movies2HDD")
mainwindow.step1 = Step1()
mainwindow.step2 = Step2()
mainwindow.step3 = Step3()
mainwindow.addPage(mainwindow.step1)
mainwindow.addPage(mainwindow.step2)
mainwindow.addPage(mainwindow.step3)
mainwindow.show()
app.exec_()
try:
	movies2hdd.disconnect()
except:
	pass
