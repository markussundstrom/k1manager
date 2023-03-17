'''
    K1Manager - A tool for transferring presets to the Kawai K1 models of synthesizers
    Copyright (C) 2022-2023 Markus Sundström

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import k1filereader
import k1midi
from k1data import K1library, K1patch
import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *


qt_creator_file = Path(__file__).parent.absolute()/'k1window.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = K1library()
        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.setFilterKeyColumn(1)
        self.singleView.setModel(self.proxyModel)
        self.sendButton.pressed.connect(self.send)
        self.refreshPortsButton.pressed.connect(self.refreshPorts)
        self.filterChoice.activated.connect(self.filterPresets)

    def send(self):
        indexes = self.singleView.selectedIndexes()
        if indexes:
            index = self.proxyModel.mapToSource(indexes[0])
            self.model.prepare_singlepatch(index,
                                        self.intextChoice.currentIndex(),
                                        self.bankChoice.currentIndex(),
                                        self.slotChoice.currentIndex(),
                                        self.portChoice.currentText(),
                                        self.channelChoice.currentIndex())

    def refreshPorts(self):
        self.portChoice.clear()
        self.portChoice.addItems(k1midi.get_midi_ports())

    def filterPresets(self):
        filterTerm = self.filterChoice.currentText()
        if (filterTerm != 'All'):
            self.proxyModel.setFilterRegExp(filterTerm)
        else:
            self.proxyModel.setFilterRegExp('')

k1midi.init_midi()
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
files = []
for f in sys.argv[1:]:
    files.append(f)
bankpath = Path(__file__).parent.absolute()/'banks'
for f in bankpath.rglob('*'):
    if (f.suffix.lower() == '.syx'):
        files.append(f)
k1filereader.read_bankfiles(files, window.model)
window.filterChoice.addItems(window.model.get_banknames())
window.show()
app.exec_()
