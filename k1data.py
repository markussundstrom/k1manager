from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import k1midi

class K1patch:
    def __init__(self, data, source):
        self.data = bytes(data)
        self.name = str(self.data[0:10], encoding='utf-8')
        self.source = source

class K1library(QtCore.QAbstractTableModel):
    def __init__(self):
        super(K1library, self).__init__()
        self.singlepatches = []
        self.multipatches = []
        self.banknames = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.singlepatches[index.row()].name
            elif index.column() == 1:
                return self.singlepatches[index.row()].source

    def rowCount(self, index):
        return len(self.singlepatches)

    def columnCount(self, index):
        return 2

    def add_single(self, patch):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(0), self.rowCount(0))
        self.singlepatches.append(patch)
        self.endInsertRows()

    def add_multi(self, patch):
        self.multipatches.append(patch)

    def add_bankname(self, name):
        self.banknames.append(name)

    def get_banknames(self):
        return self.banknames

    def prepare_singlepatch(self, index, ie, bank, slot, port, channel):
        k1midi.connect_port(port)

        message = bytearray()
        message.extend(b'\xF0\x40')
        message.append(channel)
        message.extend(b'\x20\x00\x03')
        message.append(ie)
        message.append((bank << 3) + slot)
        message.extend(self.singlepatches[index.row()].data)
        message.extend(b'\xF7')
        k1midi.send_message(message)
