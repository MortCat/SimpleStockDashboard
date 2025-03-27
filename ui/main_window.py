# taiwan_stock_dashboard/ui/main_window.py

import threading
from PyQt5.QtWidgets import (
    QMainWindow, QTableView, QVBoxLayout, QWidget,
    QMessageBox, QMenu, QAction, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPalette, QColor
from model.stock_model import StockTableModel
from service.stock_service import load_stock_list, save_stock_list, fetch_stock_data

class StockMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Dashboard")
        self.resize(720, 320)

        self.table = QTableView()
        self.model = StockTableModel([])
        self.table.setModel(self.model)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.set_dark_theme()

        self.stock_list = load_stock_list()
        if not self.stock_list:
            QMessageBox.critical(self, "Error", "No Stock ID found in stocks.json, Please add stock id and restart application.")
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(30000)

        self.update_data()

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #E0E0E0;
                font-size: 14px;
                font-family: 'Segoe UI', '微軟正黑體';
            }
            QHeaderView::section {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c2c2c, stop:1 #3c3c3c
                );
                color: white;
                padding: 4px;
                border: 1px solid #444;
            }
            QTableView {
                gridline-color: #444;
                selection-background-color: #2a82da;
                selection-color: white;
                background-color: #1e1e1e;
                alternate-background-color: #2a2a2a;
            }
            QTableView QTableCornerButton::section {
                background-color: #2c2c2c;
                border: 1px solid #444;
            }
        """)

    def show_context_menu(self, pos: QPoint):
        menu = QMenu(self)
        setting_action = QAction("List Setting", self)
        setting_action.triggered.connect(self.edit_stock_list)
        menu.addAction(setting_action)
        menu.exec_(self.table.mapToGlobal(pos))

    def edit_stock_list(self):
        current_list = ",".join(self.stock_list)
        text, ok = QInputDialog.getText(self, "Enter StockID（Separated by commas）", "Stock ID:", text=current_list)
        if ok:
            new_list = [s.strip() for s in text.split(',') if s.strip()]
            self.stock_list = new_list
            save_stock_list(new_list)
            self.update_data()

    def update_data(self):
        def worker():
            result = fetch_stock_data(self.stock_list)
            self.model = StockTableModel(result)
            self.table.setModel(self.model)

        threading.Thread(target=worker).start()
