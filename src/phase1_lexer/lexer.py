from .token_definitions import TokenType
from .symbol_table import SymbolTable
from .error_handler import ErrorHandler


class Token:
    def __init__(self, token_type, lexeme, line, column):
        self.type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column


class LexicalAnalyzer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.symbol_table = SymbolTable()
        self.errors = ErrorHandler()
        self.keywords = {
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES',
            'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'INT',
            'FLOAT', 'TEXT', 'AND', 'OR', 'NOT'
        }


    def current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]


    def advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1


    def peek_char(self, offset=1):
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]


    # Skip whitespace
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()


    # Skip single line comment --
    def skip_single_line_comment(self):
        self.advance()
        self.advance()
        while self.current_char() and self.current_char() != '\n':
            self.advance()
        if self.current_char() == '\n':
            self.advance()


    # Skip multi-line comment ##
    def skip_multi_line_comment(self):
        start_line = self.line
        self.advance()
        while self.current_char():
            if self.current_char() == '#':
                self.advance()
                return
            self.advance()
        self.errors.add_error("Unclosed comment", start_line)


    # String literal
    def read_string(self):
        start_line = self.line
        start_col = self.column
        value = "'"
        self.advance()
        while self.current_char() and self.current_char() != "'":
            if self.current_char() == '\n':
                self.errors.add_error("Unclosed string", start_line)
                return None
            value += self.current_char()
            self.advance()
        if self.current_char() == "'":
            value += "'"
            self.advance()
            return Token(TokenType.STRING_LITERAL, value, start_line, start_col)
        self.errors.add_error("Unclosed string", start_line)
        return None


    # Number literal
    def read_number(self):
        start_line = self.line
        start_col = self.column
        value = ""
        has_decimal = False
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_decimal:
                    break
                has_decimal = True
            value += self.current_char()
            self.advance()
        token_type = TokenType.FLOAT_LITERAL if has_decimal else TokenType.INT_LITERAL
        return Token(token_type, value, start_line, start_col)


    # Identifier or keyword (CORRECTED: Case-insensitive keyword matching)
    def read_identifier_or_keyword(self):
        start_line = self.line
        start_col = self.column
        value = ""
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            value += self.current_char()
            self.advance()
        
        # Convert to uppercase for keyword comparison (case-insensitive)
        if value.upper() in self.keywords:
            return Token(TokenType.KEYWORD, value, start_line, start_col)
        else:
            self.symbol_table.add(value, start_line, start_col)
            return Token(TokenType.IDENTIFIER, value, start_line, start_col)


    # Operator (arithmetic + comparison)
    def read_operator(self):
        start_line = self.line
        start_col = self.column
        char = self.current_char()
        next_char = self.peek_char()
        op = char


        # Two-character operators: >=, <=, !=, <>
        if char in ['>', '<', '!'] and next_char == '=':
            op += next_char
            self.advance()
        elif char == '<' and next_char == '>':
            op += next_char
            self.advance()


        self.advance()
        return Token(TokenType.OPERATOR, op, start_line, start_col)


    # Main tokenizer
    def tokenize(self):
        while self.current_char():
            self.skip_whitespace()
            if not self.current_char():
                break
            char = self.current_char()


            # Comments
            if char == '-' and self.peek_char() == '-':
                self.skip_single_line_comment()
                continue
            if char == '#':
                self.skip_multi_line_comment()
                continue


            # String
            if char == "'":
                token = self.read_string()
                if token:
                    self.tokens.append(token)
                continue


            # Number
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue


            # Identifier or keyword
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier_or_keyword())
                continue


            # Operator
            if char in '+-*/%=><!':
                token = self.read_operator()
                self.tokens.append(token)
                continue


            # Delimiters
            delimiters = {'(': 'lpar', ')': 'rpar', ',': 'comma', ';': 'semicolon', '.': 'dot'}
            if char in delimiters:
                self.tokens.append(Token(TokenType.PUNCTUATION, char, self.line, self.column))
                self.advance()
                continue


            # Invalid character
            self.errors.add_error(f"Invalid character '{char}'", self.line, self.column)
            self.advance()


        return self.tokens
