from phase1_lexer.lexer import LexicalAnalyzer
from phase1_lexer.token_definitions import TokenType
from phase2_parser.parser import SyntaxAnalyzer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.theme import Theme
from rich.tree import Tree

# Define a custom soft, modern theme 
custom_theme = Theme({
    "header": "bold orchid",
    "keyword": "medium_purple3",
    "identifier": "plum1",
    "success": "pale_green3",
    "error": "light_salmon1",
    "accent": "deep_sky_blue3",
    "info": "light_steel_blue",
    "border": "bright_magenta",
})

console = Console(theme=custom_theme)

def print_tokens(tokens):
    table = Table(title="Lexical Tokens", header_style="header")
    table.add_column("Type", style="keyword", no_wrap=True)
    table.add_column("Lexeme", style="white")
    table.add_column("Line", justify="right", style="accent")
    table.add_column("Column", justify="right", style="accent")

    for token in tokens:
        table.add_row(token.type.value, token.lexeme, str(token.line), str(token.column))
    
    console.print(table)

def print_symbol_table(symbol_table):
    table = Table(title="Symbol Table", header_style="header")
    table.add_column("Identifier", style="identifier")
    table.add_column("First Line", justify="right", style="accent")
    table.add_column("First Column", justify="right", style="accent")
    table.add_column("Occurrences", justify="right", style="error")

    all_symbols = symbol_table.all_symbols()
    if not all_symbols:
        console.print("[info]No identifiers found.[/info]")
        return

    for identifier, info in all_symbols.items():
        table.add_row(identifier, str(info["first_line"]), str(info["first_column"]), str(info["occurrences"]))
    
    console.print(table)

def print_errors(error_handler, error_type="Lexical"):
    if not error_handler.has_errors():
        console.print(Panel.fit(f"[success]No {error_type.lower()} errors found[/success]", border_style="pale_green3"))
    else:
        table = Table(title=f"{error_type} Errors", header_style="error")
        table.add_column("Line", justify="right", style="accent")
        table.add_column("Column", justify="right", style="accent")
        table.add_column("Message", style="error")
        for err in error_handler.get_errors():
            line = str(err.get("line", "N/A"))
            col = str(err.get("column", "N/A"))
            table.add_row(line, col, err["message"])
        console.print(table)

def print_parse_tree(parse_tree):
    """Print the parse tree in a visual format"""
    if parse_tree is None:
        console.print("[error]No parse tree generated[/error]")
        return
    
    tree = Tree(f"[header]{parse_tree.node_type}[/header]")
    
    def add_children(node, tree_node):
        """Recursively add children to the tree"""
        for child in node.children:
            if child.value:
                label = f"[identifier]{child.node_type}[/identifier]: [white]{child.value}[/white]"
            else:
                label = f"[identifier]{child.node_type}[/identifier]"
            
            if child.line and child.column:
                label += f" [dim](L:{child.line}, C:{child.column})[/dim]"
            
            child_tree = tree_node.add(label)
            add_children(child, child_tree)
    
    add_children(parse_tree, tree)
    console.print(tree)

def main():
    console.print(Panel.fit("[header]Mini SQL Compiler - Phase 1 & 2: Lexical & Syntax Analysis[/header]", border_style="border"))

    # Path to your SQL test input
    sql_file_path = "src/phase1_lexer/test_input.sql"

    try:
        with open(sql_file_path, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        console.print(f"[error]Error:[/error] Cannot find [accent]{sql_file_path}[/accent]")
        return

    # ========== PHASE 1: LEXICAL ANALYSIS ==========
    console.print("\n[header]================================================================[/header]")
    console.print("[header]PHASE 1: LEXICAL ANALYSIS[/header]")
    console.print("[header]================================================================[/header]\n")
    
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()

    # Output Phase 1 results
    console.print("\n[header]=== TOKENS ===[/header]")
    print_tokens(tokens)

    console.print("\n[header]=== SYMBOL TABLE ===[/header]")
    print_symbol_table(lexer.symbol_table)

    console.print("\n[header]=== LEXICAL ERRORS ===[/header]")
    print_errors(lexer.errors, "Lexical")

    # ========== PHASE 2: SYNTAX ANALYSIS ==========
    console.print("\n[header]================================================================[/header]")
    console.print("[header]PHASE 2: SYNTAX ANALYSIS[/header]")
    console.print("[header]================================================================[/header]\n")
    
    # Filter out comments and errors from tokens for parser
    filtered_tokens = [t for t in tokens if t.type not in [TokenType.COMMENT, TokenType.ERROR]]
    
    # Initialize and run the parser
    parser = SyntaxAnalyzer(filtered_tokens)
    parse_tree = parser.parse()

    # Output Phase 2 results
    console.print("\n[header]=== PARSE TREE ===[/header]")
    print_parse_tree(parse_tree)

    console.print("\n[header]=== SYNTAX ERRORS ===[/header]")
    print_errors(parser.errors, "Syntax")

    # Summary
    console.print("\n[header]================================================================[/header]")
    if not lexer.errors.has_errors() and not parser.errors.has_errors():
        console.print(Panel.fit("[success]Lexical Analysis: PASSED\nSyntax Analysis: PASSED\n\nAll phases completed successfully![/success]", border_style="border"))
    else:
        if lexer.errors.has_errors():
            console.print("[error]Lexical Analysis: FAILED[/error]")
        else:
            console.print("[success]Lexical Analysis: PASSED[/success]")
        
        if parser.errors.has_errors():
            console.print("[error]Syntax Analysis: FAILED[/error]")
        else:
            console.print("[success]Syntax Analysis: PASSED[/success]")

if __name__ == "__main__":
    main()
