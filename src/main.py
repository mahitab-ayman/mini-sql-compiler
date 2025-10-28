from phase1_lexer.lexer import LexicalAnalyzer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.theme import Theme

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
    table = Table(title="Lexical Tokens ✨", header_style="header")
    table.add_column("Type", style="keyword", no_wrap=True)
    table.add_column("Lexeme", style="white")
    table.add_column("Line", justify="right", style="accent")
    table.add_column("Column", justify="right", style="accent")

    for token in tokens:
        table.add_row(token.type.value, token.lexeme, str(token.line), str(token.column))
    
    console.print(table)

def print_symbol_table(symbol_table):
    table = Table(title="Symbol Table ✨", header_style="header")
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

def print_errors(error_handler):
    if not error_handler.has_errors():
        console.print(Panel.fit("[success]No lexical errors found ✓[/success]", border_style="pale_green3"))
    else:
        table = Table(title="Errors 💥", header_style="error")
        table.add_column("Line", justify="right", style="accent")
        table.add_column("Message", style="error")
        for err in error_handler.get_errors():
            table.add_row(str(err["line"]), err["message"])
        console.print(table)

def main():
    console.print(Panel.fit("✨ [header]Mini SQL Compiler — Phase 1: Lexical Analysis[/header] ✨", border_style="border"))

    # Path to your SQL test input
    sql_file_path = "src/phase1_lexer/test_input.sql"

    try:
        with open(sql_file_path, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        console.print(f"[error]Error:[/error] Cannot find [accent]{sql_file_path}[/accent]")
        return

    # Initialize and run the lexer
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()

    # Output results
    console.print("\n[header]=== TOKENS ===[/header]")
    print_tokens(tokens)

    console.print("\n[header]=== SYMBOL TABLE ===[/header]")
    print_symbol_table(lexer.symbol_table)

    console.print("\n[header]=== ERRORS ===[/header]")
    print_errors(lexer.errors)

    console.print(Panel.fit("[success]Lexical Analysis Completed Successfully 💫[/success]", border_style="border"))

if __name__ == "__main__":
    main()
