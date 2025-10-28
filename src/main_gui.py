import sys
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
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #61dafb;")  # light blue accent

        # SQL input
        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("Type or paste your SQL code here...")
        self.sql_input.setFont(QFont("Consolas", 12))
        self.sql_input.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #e8e8e8;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
            }
        """)

        # Buttons
        button_layout = QHBoxLayout()

        run_button = QPushButton("Run Lexical Analysis")
        run_button.clicked.connect(self.run_lexer)
        run_button.setFixedHeight(40)
        run_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1593e3;
            }
        """)

        load_button = QPushButton("Load SQL File")
        load_button.clicked.connect(self.load_file)
        load_button.setFixedHeight(40)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: #cccccc;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)

        button_layout.addWidget(run_button)
        button_layout.addWidget(load_button)

        # Tabs
        self.tabs = QTabWidget()
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
        """Apply modern dark theme like VS Code."""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor("#252526"))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor("#e8e8e8"))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor("#007acc"))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
        self.setPalette(dark_palette)

    def create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QHeaderView::section {
                background-color: #252526;
                color: #61dafb;
                font-weight: bold;
                border: none;
                padding: 6px;
            }
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #2d2d30;
                color: #dcdcdc;
                gridline-color: #3c3c3c;
                selection-background-color: #094771;
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = LexicalAnalyzerGUI()
    gui.show()
    sys.exit(app.exec())
