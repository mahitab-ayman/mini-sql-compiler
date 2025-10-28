import sys, csv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
    QLabel, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
from phase1_lexer.lexer import LexicalAnalyzer


class LexicalAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini SQL Compiler — Lexical Analyzer")
        self.setGeometry(200, 100, 1100, 750)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Mini SQL Compiler — Phase 1: Lexical Analysis")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("JetBrains Mono", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #4da6ff;")  # professional blue accent

        # SQL input
        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("Type or paste your SQL code here...")
        self.sql_input.setFont(QFont("Consolas", 12))
        self.sql_input.setStyleSheet("""
            QTextEdit {
                background-color: #111111;
                color: #e0e0e0;
                border: 1px solid #333333;
                border-radius: 6px;
            }
        """)

        # Buttons
        button_layout = QHBoxLayout()

        button_style = """
            QPushButton {
                background-color: transparent;
                color: #4da6ff;
                font-weight: bold;
                border: 1px solid #4da6ff;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4da6ff;
                color: #111111;
                border: 1px solid #4da6ff;
            }
        """

        run_button = QPushButton("Run Lexical Analysis")
        run_button.clicked.connect(self.run_lexer)
        run_button.setFixedHeight(40)
        run_button.setStyleSheet(button_style)

        load_button = QPushButton("Load SQL File")
        load_button.clicked.connect(self.load_file)
        load_button.setFixedHeight(40)
        load_button.setStyleSheet(button_style)

        save_button = QPushButton("Save Results as CSV")
        save_button.clicked.connect(self.save_as_csv)
        save_button.setFixedHeight(40)
        save_button.setStyleSheet(button_style)

        button_layout.addWidget(run_button)
        button_layout.addWidget(load_button)
        button_layout.addWidget(save_button)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #111111;
                color: #cccccc;
                padding: 8px 16px;
                border: 1px solid #333333;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #4da6ff;
                border: 1px solid #4da6ff;
                border-bottom: none;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                top: -1px;
                background-color: #1e1e1e;
            }
        """)

        self.tokens_table = self.create_table(["Type", "Lexeme", "Line", "Column"])
        self.symbol_table = self.create_table(["Identifier", "First Line", "First Column", "Occurrences"])
        self.errors_table = self.create_table(["Line", "Message"])

        self.tabs.addTab(self.tokens_table, "Tokens")
        self.tabs.addTab(self.symbol_table, "Symbol Table")
        self.tabs.addTab(self.errors_table, "Errors")

        layout.addWidget(title)
        layout.addWidget(self.sql_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.apply_dark_theme()

    def apply_dark_theme(self):
        """Apply modern dark theme similar to Visual Studio Code."""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor("#0f0f0f"))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor("#1a1a1a"))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor("#e0e0e0"))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor("#1a1a1a"))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#4da6ff"))
        self.setPalette(dark_palette)

    def create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #4da6ff;
                font-weight: bold;
                border: none;
                padding: 6px;
            }
            QTableWidget {
                background-color: #111111;
                alternate-background-color: #1a1a1a;
                color: #dcdcdc;
                gridline-color: #333333;
                selection-background-color: #003366;
            }
        """)
        table.horizontalHeader().setStretchLastSection(True)
        return table

    def run_lexer(self):
        source_code = self.sql_input.toPlainText()
        if not source_code.strip():
            QMessageBox.warning(self, "No Input", "Please enter or load SQL code before running.")
            return

        lexer = LexicalAnalyzer(source_code)
        tokens = lexer.tokenize()

        self.fill_tokens(tokens)
        self.fill_symbols(lexer.symbol_table.all_symbols())

        try:
            errors = lexer.errors.get_errors()
        except Exception:
            errors = getattr(lexer.errors, "errors", [])
        self.fill_errors(errors)

    def fill_tokens(self, tokens):
        self.tokens_table.setRowCount(len(tokens))
        for i, token in enumerate(tokens):
            self.tokens_table.setItem(i, 0, QTableWidgetItem(token.type.value))
            self.tokens_table.setItem(i, 1, QTableWidgetItem(token.lexeme))
            self.tokens_table.setItem(i, 2, QTableWidgetItem(str(token.line)))
            self.tokens_table.setItem(i, 3, QTableWidgetItem(str(token.column)))
        self.tokens_table.resizeColumnsToContents()

    def fill_symbols(self, symbols):
        items = list(symbols.items())
        self.symbol_table.setRowCount(len(items))
        for i, (identifier, info) in enumerate(items):
            self.symbol_table.setItem(i, 0, QTableWidgetItem(identifier))
            self.symbol_table.setItem(i, 1, QTableWidgetItem(str(info.get("first_line", ""))))
            self.symbol_table.setItem(i, 2, QTableWidgetItem(str(info.get("first_column", ""))))
            self.symbol_table.setItem(i, 3, QTableWidgetItem(str(info.get("occurrences", 0))))
        self.symbol_table.resizeColumnsToContents()

    def fill_errors(self, errors):
        self.errors_table.setRowCount(len(errors))
        for i, err in enumerate(errors):
            if isinstance(err, dict):
                line = str(err.get("line", ""))
                msg = err.get("message", str(err))
            else:
                line = ""
                msg = str(err)
            self.errors_table.setItem(i, 0, QTableWidgetItem(line))
            self.errors_table.setItem(i, 1, QTableWidgetItem(msg))
        self.errors_table.resizeColumnsToContents()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open SQL File", "", "SQL Files (*.sql);;All Files (*)"
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.sql_input.setPlainText(f.read())

    def save_as_csv(self):
        current_tab = self.tabs.currentWidget()
        tab_name = self.tabs.tabText(self.tabs.currentIndex())
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Save {tab_name} as CSV",
            f"{tab_name.lower().replace(' ', '_')}.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                headers = [
                    current_tab.horizontalHeaderItem(i).text()
                    for i in range(current_tab.columnCount())
                ]
                writer.writerow(headers)

                for row in range(current_tab.rowCount()):
                    row_data = [
                        current_tab.item(row, col).text() if current_tab.item(row, col) else ""
                        for col in range(current_tab.columnCount())
                    ]
                    writer.writerow(row_data)

            QMessageBox.information(
                self,
                "Success",
                f"{tab_name} has been saved successfully as CSV!\n\n{file_path}",
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save {tab_name}.\nError: {str(e)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = LexicalAnalyzerGUI()
    gui.show()
    sys.exit(app.exec())
