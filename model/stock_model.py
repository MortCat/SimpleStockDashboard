# taiwan_stock_dashboard/model/stock_model.py

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor

class StockTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.headers = ['Stock ID', 'Name', 'Current Price', 'Change %', 'Previous Close', 'Volume', 'Open Price']

    def rowCount(self, index): return len(self._data)
    def columnCount(self, index): return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        value = self._data[row][col]

        if role == Qt.DisplayRole:
            return value
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.ForegroundRole and col == 3:
            try:
                pct = float(value.replace('%', ''))
                if pct > 0: return QColor("red")
                elif pct < 0: return QColor("green")
            except: pass
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return self.headers[section] if orientation == Qt.Horizontal else str(section + 1)
