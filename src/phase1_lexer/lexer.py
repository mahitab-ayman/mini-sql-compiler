from .token_definitions import TokenType
from .symbol_table import SymbolTable
from .error_handler import ErrorHandler

KEYWORDS = {
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
    "UPDATE", "SET", "DELETE", "CREATE", "TABLE", "INT",
    "FLOAT", "TEXT", "AND", "OR", "NOT"
}

class Token:
    def __init__(self, ttype, lexeme, line, col):
        self.type = ttype
        self.lexeme = lexeme
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.line}:{self.col} {self.type.name} {self.lexeme!r}"

class LexicalAnalyzer:
    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens = []
        self.symtab = SymbolTable()
        self.errors = ErrorHandler()

    def analyze(self):
        while self.pos < len(self.text):
            c = self.text[self.pos]
            if c.isspace():
                self._consume_whitespace()
                continue
            if c.isalpha():
                start_col = self.col
                lex = self._consume_identifier()
                ttype = TokenType.KEYWORD if lex in KEYWORDS else TokenType.IDENTIFIER
                token = Token(ttype, lex, self.line, start_col)
                self.tokens.append(token)
                if ttype == TokenType.IDENTIFIER:
                    self.symtab.add(lex, self.line, start_col)
                continue
            token = Token(TokenType.PUNCTUATION, c, self.line, self.col)
            self.tokens.append(token)
            self._advance()
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))

    def _advance(self):
        if self.pos < len(self.text):
            if self.text[self.pos] == '\\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1

    def _consume_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self._advance()

    def _consume_identifier(self):
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
            self._advance()
        return self.text[start:self.pos]

    def display_tokens(self):
        for t in self.tokens:
            print(t)

    def display_symtab(self):
        for k, v in self.symtab.table.items():
            print(f"{k} -> {v}")
