import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from model.regression import RegressionPricingModel
from scraper.competitor_scraper import CompetitorPriceScraper

SAMPLE_DATA = pd.DataFrame({
    'demand': [100, 150, 200, 250, 300],
    'time': [1, 2, 3, 4, 5],
    'competitor_price': [10, 12, 11, 13, 12],
    'actual_price': [11, 13, 12, 14, 13]
})

class PricingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('💸 Dynamic Pricing Engine')
        self.resize(950, 650)
        self.df = SAMPLE_DATA.copy()
        self.set_dark_theme()
        self.init_ui()

    def set_dark_theme(self):
        # Softer blue: #4FC3F7
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.WindowText, QColor(160, 210, 255))
        dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(40, 40, 40))
        dark_palette.setColor(QPalette.ToolTipText, QColor(160, 210, 255))
        dark_palette.setColor(QPalette.Text, QColor(160, 210, 255))
        dark_palette.setColor(QPalette.Button, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ButtonText, QColor(160, 210, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 80, 80))
        dark_palette.setColor(QPalette.Highlight, QColor(79, 195, 247))
        dark_palette.setColor(QPalette.HighlightedText, QColor(20, 20, 20))
        QApplication.instance().setPalette(dark_palette)

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel('💸 Dynamic Pricing Engine')
        title.setFont(QFont('Segoe UI', 24, QFont.Bold))
        title.setStyleSheet('color: #4FC3F7; margin-bottom: 8px; background: transparent;')
        layout.addWidget(title)
        subtitle = QLabel('AI-powered price suggestions for your products — maximize your revenue with style!')
        subtitle.setFont(QFont('Segoe UI', 12))
        subtitle.setStyleSheet('color: #8ecae6; margin-bottom: 16px; background: transparent;')
        layout.addWidget(subtitle)

        # File upload
        btn_load = QPushButton('📂 Upload CSV')
        btn_load.setStyleSheet('background-color: #23272e; color: #4FC3F7; font-weight: bold;')
        btn_load.clicked.connect(self.load_csv)
        layout.addWidget(btn_load)

        # Table
        self.table = QTableWidget()
        self.table.setStyleSheet('''
            QTableWidget {
                background-color: #181a1b;
                color: #b3e0ff;
                gridline-color: #222;
                selection-background-color: #4FC3F7;
                selection-color: #181a1b;
                alternate-background-color: #23272e;
            }
            QHeaderView::section {
                background-color: #23272e;
                color: #4FC3F7;
                border: none;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #23272e;
                border: none;
            }
            QTableWidget QTableView {
                background-color: #181a1b;
            }
            QTableWidget QTableView QLineEdit, QTableWidget QLineEdit {
                background: #23272e;
                color: #b3e0ff;
                border: 1px solid #333;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23272e;
            }
        ''')
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.update_table()

        # Competitor URLs
        label_urls = QLabel('Enter competitor product URLs (one per line):')
        label_urls.setStyleSheet('color: #b3e0ff; background: transparent;')
        layout.addWidget(label_urls)
        self.url_text = QTextEdit()
        self.url_text.setStyleSheet('background-color: #23272e; color: #b3e0ff; border: 1px solid #333;')
        layout.addWidget(self.url_text)
        btn_scrape = QPushButton('🌐 Scrape Competitor Prices')
        btn_scrape.setStyleSheet('background-color: #23272e; color: #4FC3F7; font-weight: bold; border: none;')
        btn_scrape.clicked.connect(self.scrape_prices)
        layout.addWidget(btn_scrape)
        self.scrape_result = QLabel()
        self.scrape_result.setStyleSheet('color: #90ee90; background: transparent;')
        layout.addWidget(self.scrape_result)

        # Run model
        btn_run = QPushButton('🚀 Suggest Prices')
        btn_run.setStyleSheet('background-color: #4FC3F7; color: #181a1b; font-weight: bold; border: none;')
        btn_run.clicked.connect(self.run_model)
        layout.addWidget(btn_run)

        self.result_label = QLabel()
        self.result_label.setStyleSheet('color: #90ee90; font-size: 16px; background: transparent;')
        layout.addWidget(self.result_label)

        btn_save = QPushButton('💾 Download Results as CSV')
        btn_save.setStyleSheet('background-color: #23272e; color: #4FC3F7; font-weight: bold; border: none;')
        btn_save.clicked.connect(self.save_csv)
        layout.addWidget(btn_save)

        footer = QLabel('© 2025 Dynamic Pricing Engine — Crafted with 💙 for smart businesses')
        footer.setStyleSheet('color: #444; margin-top: 24px; font-size: 11px; background: transparent;')
        layout.addWidget(footer)

        self.setLayout(layout)

    def update_table(self):
        df = self.df
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
        self.table.resizeColumnsToContents()

    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV Files (*.csv)')
        if path:
            try:
                self.df = pd.read_csv(path)
                self.update_table()
                QMessageBox.information(self, 'Success', 'Data uploaded successfully!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to load CSV: {e}')

    def scrape_prices(self):
        urls = [u.strip() for u in self.url_text.toPlainText().splitlines() if u.strip()]
        if not urls:
            QMessageBox.warning(self, 'Warning', 'Please enter at least one URL.')
            return
        scraper = CompetitorPriceScraper(urls)
        prices = scraper.scrape_prices()
        self.scrape_result.setText(str(prices))

    def run_model(self):
        required = {'demand', 'time', 'competitor_price', 'actual_price'}
        if not required.issubset(self.df.columns):
            QMessageBox.warning(self, 'Error', f'Data must include columns: {", ".join(required)}')
            return
        X = self.df[['demand', 'time', 'competitor_price']]
        y = self.df['actual_price']
        model = RegressionPricingModel()
        model.train(X, y)
        suggested = model.predict(X)
        self.df['suggested_price'] = np.round(suggested, 2)
        # Do NOT overwrite actual_price with suggested_price
        self.update_table()
        self.result_label.setText('✨ Suggested prices calculated! Your products are now priced like a pro!')

    def save_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Save CSV', '', 'CSV Files (*.csv)')
        if path:
            try:
                self.df.to_csv(path, index=False)
                QMessageBox.information(self, 'Success', 'Results saved!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to save CSV: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = PricingApp()
    win.show()
    sys.exit(app.exec_())
