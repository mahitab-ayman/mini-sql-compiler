import sys, csv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
    QLabel, QFileDialog, QHBoxLayout, QMessageBox, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
from phase1_lexer.lexer import LexicalAnalyzer
from phase1_lexer.token_definitions import TokenType
from phase2_parser.parser import SyntaxAnalyzer


class LexicalAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini SQL Compiler — Phase 1 & 2: Lexical & Syntax Analysis")
        self.setGeometry(200, 100, 1200, 800)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Mini SQL Compiler — Phase 1 & 2: Lexical & Syntax Analysis")
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

        run_button = QPushButton("Run Analysis (Phase 1 & 2)")
        run_button.clicked.connect(self.run_analysis)
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

        # Phase 1 tables
        self.tokens_table = self.create_table(["Type", "Lexeme", "Line", "Column"])
        self.symbol_table = self.create_table(["Identifier", "First Line", "First Column", "Occurrences"])
        self.lexical_errors_table = self.create_table(["Line", "Column", "Message"])
        
        # Phase 2 components
        self.parse_tree_widget = self.create_parse_tree_widget()
        self.syntax_errors_table = self.create_table(["Line", "Column", "Message"])

        # Add tabs
        self.tabs.addTab(self.tokens_table, "Tokens (Phase 1)")
        self.tabs.addTab(self.symbol_table, "Symbol Table (Phase 1)")
        self.tabs.addTab(self.lexical_errors_table, "Lexical Errors")
        self.tabs.addTab(self.parse_tree_widget, "Parse Tree (Phase 2)")
        self.tabs.addTab(self.syntax_errors_table, "Syntax Errors (Phase 2)")

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

    def create_parse_tree_widget(self):
        """Create a tree widget for displaying the parse tree"""
        tree = QTreeWidget()
        tree.setHeaderLabel("Parse Tree Structure")
        tree.setRootIsDecorated(True)  # Show tree lines
        tree.setAlternatingRowColors(True)
        tree.setIndentation(20)  # Indentation for child nodes
        tree.setStyleSheet("""
            QTreeWidget {
                background-color: #111111;
                color: #dcdcdc;
                border: 1px solid #333333;
                font-family: Consolas;
                font-size: 11px;
                show-decoration-selected: 1;
            }
            QTreeWidget::item {
                padding: 4px;
                border: none;
            }
            QTreeWidget::item:selected {
                background-color: #003366;
                color: #4da6ff;
            }
            QTreeWidget::item:hover {
                background-color: #1a1a2e;
            }
            QTreeWidget::branch {
                background-color: #111111;
            }
            QTreeWidget::branch:has-siblings:!adjoins-item {
                border-image: url(vline.png) 0;
            }
            QTreeWidget::branch:has-siblings:adjoins-item {
                border-image: url(branch-more.png) 0;
            }
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {
                border-image: url(branch-end.png) 0;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(branch-closed.png);
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                border-image: none;
                image: url(branch-open.png);
            }
        """)
        return tree

    def run_analysis(self):
        source_code = self.sql_input.toPlainText()
        if not source_code.strip():
            QMessageBox.warning(self, "No Input", "Please enter or load SQL code before running.")
            return

        # ========== PHASE 1: LEXICAL ANALYSIS ==========
        lexer = LexicalAnalyzer(source_code)
        tokens = lexer.tokenize()

        self.fill_tokens(tokens)
        self.fill_symbols(lexer.symbol_table.all_symbols())

        try:
            lexical_errors = lexer.errors.get_errors()
        except Exception:
            lexical_errors = getattr(lexer.errors, "errors", [])
        self.fill_lexical_errors(lexical_errors)

        # ========== PHASE 2: SYNTAX ANALYSIS ==========
        # Filter out comments and errors from tokens for parser
        filtered_tokens = [t for t in tokens if t.type not in [TokenType.COMMENT, TokenType.ERROR]]
        
        # Initialize and run the parser
        parser = SyntaxAnalyzer(filtered_tokens)
        parse_tree = parser.parse()
        
        # Display parse tree
        self.fill_parse_tree(parse_tree)
        
        # Display syntax errors
        try:
            syntax_errors = parser.errors.get_errors()
        except Exception:
            syntax_errors = getattr(parser.errors, "errors", [])
        self.fill_syntax_errors(syntax_errors)

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

    def fill_lexical_errors(self, errors):
        self.lexical_errors_table.setRowCount(len(errors))
        for i, err in enumerate(errors):
            if isinstance(err, dict):
                line = str(err.get("line", ""))
                column = str(err.get("column", ""))
                msg = err.get("message", str(err))
            else:
                line = ""
                column = ""
                msg = str(err)
            self.lexical_errors_table.setItem(i, 0, QTableWidgetItem(line))
            self.lexical_errors_table.setItem(i, 1, QTableWidgetItem(column))
            self.lexical_errors_table.setItem(i, 2, QTableWidgetItem(msg))
        self.lexical_errors_table.resizeColumnsToContents()

    def fill_syntax_errors(self, errors):
        self.syntax_errors_table.setRowCount(len(errors))
        for i, err in enumerate(errors):
            if isinstance(err, dict):
                line = str(err.get("line", ""))
                column = str(err.get("column", ""))
                msg = err.get("message", str(err))
            else:
                line = ""
                column = ""
                msg = str(err)
            self.syntax_errors_table.setItem(i, 0, QTableWidgetItem(line))
            self.syntax_errors_table.setItem(i, 1, QTableWidgetItem(column))
            self.syntax_errors_table.setItem(i, 2, QTableWidgetItem(msg))
        self.syntax_errors_table.resizeColumnsToContents()

    def fill_parse_tree(self, parse_tree):
        """Fill the parse tree widget with the parse tree structure"""
        self.parse_tree_widget.clear()
        
        if parse_tree is None:
            root_item = QTreeWidgetItem(self.parse_tree_widget)
            root_item.setText(0, "No parse tree generated")
            root_item.setForeground(0, QColor("#ff6b6b"))
            return
        
        def add_tree_node(parent_item, node):
            """Recursively add nodes to the tree widget"""
            # Create tree item
            item = QTreeWidgetItem(parent_item)
            
            # Format the label
            if node.value:
                label = f"{node.node_type}: {node.value}"
            else:
                label = node.node_type
            
            # Add position info if available (as part of label)
            if node.line and node.column:
                label += f" [L:{node.line}, C:{node.column}]"
            
            item.setText(0, label)
            
            # Color code by node type for better visualization
            if "STMT" in node.node_type:
                item.setForeground(0, QColor("#4da6ff"))  # Blue for statements
            elif "CONDITION" in node.node_type or "COMPARISON" in node.node_type:
                item.setForeground(0, QColor("#ffd93d"))  # Yellow for conditions
            elif "EXPRESSION" in node.node_type or "TERM" in node.node_type or "FACTOR" in node.node_type:
                item.setForeground(0, QColor("#6bcf7f"))  # Green for expressions
            elif node.node_type == "IDENTIFIER":
                item.setForeground(0, QColor("#ff6b9d"))  # Pink for identifiers
            elif node.node_type == "LITERAL":
                item.setForeground(0, QColor("#c44569"))  # Purple for literals
            elif "OPERATOR" in node.node_type or node.node_type == "DATA_TYPE":
                item.setForeground(0, QColor("#feca57"))  # Orange for operators/types
            else:
                item.setForeground(0, QColor("#dcdcdc"))  # Default white
            
            # Recursively add children
            for child in node.children:
                add_tree_node(item, child)
        
        # Create root item
        root_item = QTreeWidgetItem(self.parse_tree_widget)
        root_label = parse_tree.node_type
        if parse_tree.value:
            root_label += f": {parse_tree.value}"
        if parse_tree.line and parse_tree.column:
            root_label += f" [L:{parse_tree.line}, C:{parse_tree.column}]"
        root_item.setText(0, root_label)
        root_item.setForeground(0, QColor("#4da6ff"))
        root_item.setFont(0, QFont("Consolas", 12, QFont.Weight.Bold))
        
        # Add all children
        for child in parse_tree.children:
            add_tree_node(root_item, child)
        
        # Expand all nodes by default to show full tree
        self.parse_tree_widget.expandAll()
        
        # Resize columns to fit content
        self.parse_tree_widget.resizeColumnToContents(0)

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
        
        # Handle parse tree widget separately (save as text file)
        if isinstance(current_tab, QTreeWidget):
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f"Save {tab_name} as Text",
                f"{tab_name.lower().replace(' ', '_')}.txt",
                "Text Files (*.txt);;All Files (*)"
            )
            if not file_path:
                return
            
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    def write_tree_item(item, indent=0):
                        file.write("  " * indent + item.text(0) + "\n")
                        for i in range(item.childCount()):
                            write_tree_item(item.child(i), indent + 1)
                    
                    root = current_tab.topLevelItem(0)
                    if root:
                        write_tree_item(root)
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"{tab_name} has been saved successfully as text file!\n\n{file_path}",
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save {tab_name}.\nError: {str(e)}"
                )
            return
        
        # Handle table widgets
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
