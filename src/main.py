from phase1_lexer.lexer import LexicalAnalyzer

def print_tokens(tokens):
    print("\n=== TOKENS ===")
    for token in tokens:
        print(f"{token.type.value:<15} | {token.lexeme:<25} | (Line {token.line}, Col {token.column})")

def print_symbol_table(symbol_table):
    print("\n=== SYMBOL TABLE ===")
    table = symbol_table.all_symbols()
    if not table:
        print("No identifiers found.")
        return
    print(f"{'Identifier':<20} | {'First Line':<10} | {'First Column':<13} | {'Occurrences'}")
    print("-" * 65)
    for identifier, info in table.items():
        print(f"{identifier:<20} | {info['first_line']:<10} | {info['first_column']:<13} | {info['occurrences']}")

def print_errors(error_handler):
    print("\n=== ERRORS ===")
    if not error_handler.has_errors():
        print("No lexical errors found.")
    else:
        for err in error_handler.get_errors():
            print(f"[Line {err['line']}] {err['message']}")

def main():
    print("=== Mini SQL Compiler — Phase 1: Lexical Analysis ===")

    # Path to your SQL test input
    sql_file_path = "phase1_lexer/test_input.sql"

    try:
        with open(sql_file_path, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: Cannot find {sql_file_path}")
        return

    # Initialize and run the lexer
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()

    # Output results
    print_tokens(tokens)
    print_symbol_table(lexer.symbol_table)
    print_errors(lexer.errors)

    print("\n=== Lexical Analysis Completed ===")

if __name__ == "__main__":
    main()
