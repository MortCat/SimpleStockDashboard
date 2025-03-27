# taiwan_stock_dashboard/main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import StockMonitor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockMonitor()
    window.show()
    sys.exit(app.exec_())
