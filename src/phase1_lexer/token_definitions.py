from enum import Enum

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INT_LITERAL = "INT_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    STRING_LITERAL = "STRING_LITERAL"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    COMMENT = "COMMENT"
    EOF = "EOF"
    ERROR = "ERROR"

KEYWORDS = {
    "SELECT", "FROM", "WHERE", "INSERT", "INTO", "VALUES",
    "UPDATE", "SET", "DELETE", "CREATE", "TABLE",
    "INT", "FLOAT", "TEXT", "AND", "OR", "NOT"
}

OPERATORS = {"+", "-", "*", "/", "=", "!=", ">", ">=", "<", "<="}

DELIMITERS = {",", ";", "(", ")"}
