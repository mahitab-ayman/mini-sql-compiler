from phase1_lexer.lexer import LexicalAnalyzer

def main():
    with open("src/phase1_lexer/test_input.sql", "r") as f:
        source = f.read()
    lexer = LexicalAnalyzer(source)
    lexer.analyze()
    print("=== Tokens ===")
    lexer.display_tokens()
    print("\\n=== Symbol Table ===")
    lexer.display_symtab()

if __name__ == "__main__":
    main()
