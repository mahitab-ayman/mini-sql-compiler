"""
Syntax Analyzer (Parser) for SQL-like Language
Implements Recursive Descent Parsing to build a Parse Tree
"""

from .parse_tree import ParseTreeNode
from phase1_lexer.token_definitions import TokenType
from phase1_lexer.error_handler import ErrorHandler


class SyntaxAnalyzer:
    """Recursive Descent Parser for SQL-like queries"""
    
    def __init__(self, tokens):
        """
        Initialize the parser with tokens from lexical analyzer
        
        Args:
            tokens: List of Token objects from Phase 1
        """
        self.tokens = tokens
        self.current_index = 0
        self.errors = ErrorHandler()
        self.parse_tree = None
    
    def current_token(self):
        """Get the current token"""
        if self.current_index >= len(self.tokens):
            return None
        return self.tokens[self.current_index]
    
    def peek_token(self, offset=1):
        """Peek at a token ahead"""
        idx = self.current_index + offset
        if idx >= len(self.tokens):
            return None
        return self.tokens[idx]
    
    def advance(self):
        """Move to the next token"""
        if self.current_index < len(self.tokens):
            self.current_index += 1
    
    def match(self, expected_type, expected_lexeme=None):
        """
        Check if current token matches expected type and optionally lexeme
        
        Args:
            expected_type: Expected TokenType
            expected_lexeme: Optional expected lexeme value
        
        Returns:
            True if match, False otherwise
        """
        token = self.current_token()
        if token is None:
            return False
        
        if token.type != expected_type:
            return False
        
        if expected_lexeme is not None and token.lexeme.upper() != expected_lexeme.upper():
            return False
        
        return True
    
    def consume(self, expected_type, expected_lexeme=None):
        """
        Consume a token if it matches, otherwise report error
        
        Args:
            expected_type: Expected TokenType
            expected_lexeme: Optional expected lexeme value
        
        Returns:
            The consumed token or None if error
        """
        token = self.current_token()
        
        if token is None:
            expected_str = f"'{expected_lexeme}'" if expected_lexeme else expected_type.value
            self.report_error(
                f"Expected {expected_str}, but found end of input",
                None, None
            )
            return None
        
        if token.type != expected_type:
            expected_str = f"'{expected_lexeme}'" if expected_lexeme else expected_type.value
            self.report_error(
                f"Expected {expected_str} at line {token.line}, position {token.column}, but found '{token.lexeme}'",
                token.line, token.column
            )
            return None
        
        if expected_lexeme is not None and token.lexeme.upper() != expected_lexeme.upper():
            self.report_error(
                f"Expected '{expected_lexeme}' at line {token.line}, position {token.column}, but found '{token.lexeme}'",
                token.line, token.column
            )
            return None
        
        self.advance()
        return token
    
    def report_error(self, message, line, column):
        """Report a syntax error with proper formatting"""
        if line is None or column is None:
            token = self.current_token()
            if token:
                line = token.line
                column = token.column
            else:
                line = 0
                column = 0
        
        # Format: "Syntax Error: Expected 'FROM' at line 5, position 12, but found 'WHERE'."
        # If message already contains "Expected", use it as is, otherwise format it
        if message.startswith("Expected"):
            # Ensure the message ends with a period
            if not message.endswith('.'):
                message = message + '.'
            self.errors.add_error(f"Syntax Error: {message}", line, column)
        else:
            self.errors.add_error(f"Syntax Error: {message} at line {line}, position {column}.", line, column)
    
    def synchronize(self):
        """
        Error recovery: skip tokens until finding a synchronizing token
        Synchronizing tokens: SEMICOLON, CREATE, SELECT, INSERT, UPDATE, DELETE
        
        For semicolons, advance past them to skip to the next statement.
        For keywords, stop so they can be parsed as the start of the next statement.
        """
        while self.current_token():
            token = self.current_token()
            
            # If we find a semicolon, advance past it and stop
            if token.type == TokenType.PUNCTUATION and token.lexeme == ';':
                self.advance()
                return
            
            # If we find a statement-starting keyword, stop (don't advance)
            # so it can be parsed as the next statement
            if token.type == TokenType.KEYWORD:
                keyword = token.lexeme.upper()
                if keyword in ['CREATE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE']:
                    return
            
            self.advance()
    
    # ==================== Grammar Rules ====================
    
    def parse(self):
        """
        Main entry point: Parse the token stream
        
        Returns:
            ParseTreeNode representing the root of the parse tree
        """
        root = ParseTreeNode("PROGRAM")
        
        while self.current_token():
            # Skip comments and errors from lexer
            token = self.current_token()
            if token.type == TokenType.COMMENT or token.type == TokenType.ERROR:
                self.advance()
                continue
            
            # Track errors before parsing statement
            error_count_before = len(self.errors.get_errors())
            
            # Parse a statement
            stmt = self.parse_statement()
            if stmt:
                root.add_child(stmt)
            
            # Check if new errors occurred during statement parsing
            error_count_after = len(self.errors.get_errors())
            if error_count_after > error_count_before:
                # Error occurred, try to recover
                self.synchronize()
            else:
                # No error, try to consume semicolon if present
                if self.match(TokenType.PUNCTUATION, ';'):
                    self.advance()
        
        self.parse_tree = root
        return root
    
    def parse_statement(self):
        """
        Parse a SQL statement
        
        Statement -> SELECT_STMT | INSERT_STMT | UPDATE_STMT | DELETE_STMT | CREATE_STMT
        """
        token = self.current_token()
        if token is None:
            return None
        
        if token.type != TokenType.KEYWORD:
            self.report_error(
                f"Expected a SQL statement keyword (SELECT, INSERT, UPDATE, DELETE, CREATE) at line {token.line}, position {token.column}, but found '{token.lexeme}'",
                token.line, token.column
            )
            return None
        
        keyword = token.lexeme.upper()
        
        if keyword == 'SELECT':
            return self.parse_select_statement()
        elif keyword == 'INSERT':
            return self.parse_insert_statement()
        elif keyword == 'UPDATE':
            return self.parse_update_statement()
        elif keyword == 'DELETE':
            return self.parse_delete_statement()
        elif keyword == 'CREATE':
            return self.parse_create_statement()
        else:
            self.report_error(
                f"Unexpected keyword '{keyword}' at line {token.line}, position {token.column}. Expected one of: SELECT, INSERT, UPDATE, DELETE, CREATE",
                token.line, token.column
            )
            return None
    
    def parse_select_statement(self):
        """
        Parse SELECT statement
        
        SELECT_STMT -> SELECT SelectList FROM Identifier [WHERE Condition]
        """
        node = ParseTreeNode("SELECT_STMT")
        start_token = self.current_token()
        node.set_position(start_token.line, start_token.column)
        
        # SELECT
        if not self.consume(TokenType.KEYWORD, 'SELECT'):
            return None
        
        # SelectList
        select_list = self.parse_select_list()
        if select_list:
            node.add_child(select_list)
        
        # FROM
        if not self.consume(TokenType.KEYWORD, 'FROM'):
            return None
        
        # Identifier (table name)
        table_node = self.parse_identifier()
        if table_node:
            node.add_child(table_node)
        else:
            return None
        
        # Optional WHERE clause
        if self.match(TokenType.KEYWORD, 'WHERE'):
            where_clause = self.parse_where_clause()
            if where_clause:
                node.add_child(where_clause)
        
        return node
    
    def parse_select_list(self):
        """
        Parse SELECT list
        
        SelectList -> '*' | ColumnList
        ColumnList -> SelectItem (',' SelectItem)*
        SelectItem -> Identifier | Expression
        """
        node = ParseTreeNode("SELECT_LIST")
        
        if self.match(TokenType.OPERATOR, '*'):
            token = self.consume(TokenType.OPERATOR, '*')
            if token:
                child = ParseTreeNode("ALL_COLUMNS", "*")
                child.set_position(token.line, token.column)
                node.add_child(child)
        else:
            # ColumnList - can be Identifier or Expression
            first_item = self.parse_select_item()
            if first_item:
                node.add_child(first_item)
            else:
                return None
            
            while self.match(TokenType.PUNCTUATION, ','):
                self.advance()  # consume comma
                item = self.parse_select_item()
                if item:
                    node.add_child(item)
                else:
                    break
        
        return node
    
    def parse_select_item(self):
        """
        Parse a select item (column or expression)
        
        SelectItem -> Identifier | Expression
        
        Note: parse_expression handles identifiers as well (Factor -> Identifier),
        so we can use it for both cases. It will stop at non-arithmetic operators
        or keywords like FROM.
        """
        # parse_expression handles both identifiers and expressions
        # It stops when it encounters a non-arithmetic operator or keyword
        return self.parse_expression()
    
    def parse_insert_statement(self):
        """
        Parse INSERT statement
        
        INSERT_STMT -> INSERT INTO Identifier VALUES '(' ValueList ')'
        """
        node = ParseTreeNode("INSERT_STMT")
        start_token = self.current_token()
        node.set_position(start_token.line, start_token.column)
        
        # INSERT
        if not self.consume(TokenType.KEYWORD, 'INSERT'):
            return None
        
        # INTO
        if not self.consume(TokenType.KEYWORD, 'INTO'):
            return None
        
        # Identifier (table name)
        table_node = self.parse_identifier()
        if table_node:
            node.add_child(table_node)
        else:
            return None
        
        # VALUES
        if not self.consume(TokenType.KEYWORD, 'VALUES'):
            return None
        
        # '('
        if not self.consume(TokenType.PUNCTUATION, '('):
            return None
        
        # ValueList
        value_list = self.parse_value_list()
        if value_list:
            node.add_child(value_list)
        else:
            return None
        
        # ')'
        if not self.consume(TokenType.PUNCTUATION, ')'):
            return None
        
        return node
    
    def parse_value_list(self):
        """
        Parse value list
        
        ValueList -> Value (',' Value)*
        Value -> Literal | Expression
        """
        node = ParseTreeNode("VALUE_LIST")
        
        value = self.parse_value()
        if value:
            node.add_child(value)
        else:
            return None
        
        while self.match(TokenType.PUNCTUATION, ','):
            self.advance()  # consume comma
            val = self.parse_value()
            if val:
                node.add_child(val)
            else:
                break
        
        return node
    
    def parse_value(self):
        """
        Parse a value
        
        Value -> Literal | Expression
        Literal -> INT_LITERAL | FLOAT_LITERAL | STRING_LITERAL
        """
        token = self.current_token()
        if token is None:
            return None
        
        if token.type in [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STRING_LITERAL]:
            node = ParseTreeNode("LITERAL", token.lexeme)
            node.set_position(token.line, token.column)
            self.advance()
            return node
        else:
            # Try to parse as expression
            return self.parse_expression()
    
    def parse_update_statement(self):
        """
        Parse UPDATE statement
        
        UPDATE_STMT -> UPDATE Identifier SET AssignmentList [WHERE Condition]
        """
        node = ParseTreeNode("UPDATE_STMT")
        start_token = self.current_token()
        node.set_position(start_token.line, start_token.column)
        
        # UPDATE
        if not self.consume(TokenType.KEYWORD, 'UPDATE'):
            return None
        
        # Identifier (table name)
        table_node = self.parse_identifier()
        if table_node:
            node.add_child(table_node)
        else:
            return None
        
        # SET
        if not self.consume(TokenType.KEYWORD, 'SET'):
            return None
        
        # AssignmentList
        assignment_list = self.parse_assignment_list()
        if assignment_list:
            node.add_child(assignment_list)
        else:
            return None
        
        # Optional WHERE clause
        if self.match(TokenType.KEYWORD, 'WHERE'):
            where_clause = self.parse_where_clause()
            if where_clause:
                node.add_child(where_clause)
        
        return node
    
    def parse_assignment_list(self):
        """
        Parse assignment list
        
        AssignmentList -> Assignment (',' Assignment)*
        Assignment -> Identifier '=' Value
        """
        node = ParseTreeNode("ASSIGNMENT_LIST")
        
        assignment = self.parse_assignment()
        if assignment:
            node.add_child(assignment)
        else:
            return None
        
        while self.match(TokenType.PUNCTUATION, ','):
            self.advance()  # consume comma
            assign = self.parse_assignment()
            if assign:
                node.add_child(assign)
            else:
                break
        
        return node
    
    def parse_assignment(self):
        """
        Parse a single assignment
        
        Assignment -> Identifier '=' Value
        """
        node = ParseTreeNode("ASSIGNMENT")
        
        # Identifier
        identifier = self.parse_identifier()
        if identifier:
            node.add_child(identifier)
        else:
            return None
        
        # '='
        if not self.consume(TokenType.OPERATOR, '='):
            return None
        
        # Value
        value = self.parse_value()
        if value:
            node.add_child(value)
        else:
            return None
        
        return node
    
    def parse_delete_statement(self):
        """
        Parse DELETE statement
        
        DELETE_STMT -> DELETE FROM Identifier [WHERE Condition]
        """
        node = ParseTreeNode("DELETE_STMT")
        start_token = self.current_token()
        node.set_position(start_token.line, start_token.column)
        
        # DELETE
        if not self.consume(TokenType.KEYWORD, 'DELETE'):
            return None
        
        # FROM
        if not self.consume(TokenType.KEYWORD, 'FROM'):
            return None
        
        # Identifier (table name)
        table_node = self.parse_identifier()
        if table_node:
            node.add_child(table_node)
        else:
            return None
        
        # Optional WHERE clause
        if self.match(TokenType.KEYWORD, 'WHERE'):
            where_clause = self.parse_where_clause()
            if where_clause:
                node.add_child(where_clause)
        
        return node
    
    def parse_create_statement(self):
        """
        Parse CREATE TABLE statement
        
        CREATE_STMT -> CREATE TABLE Identifier '(' ColumnDefList ')'
        """
        node = ParseTreeNode("CREATE_STMT")
        start_token = self.current_token()
        node.set_position(start_token.line, start_token.column)
        
        # CREATE
        if not self.consume(TokenType.KEYWORD, 'CREATE'):
            return None
        
        # TABLE
        if not self.consume(TokenType.KEYWORD, 'TABLE'):
            return None
        
        # Identifier (table name)
        table_node = self.parse_identifier()
        if table_node:
            node.add_child(table_node)
        else:
            return None
        
        # '('
        if not self.consume(TokenType.PUNCTUATION, '('):
            return None
        
        # ColumnDefList
        column_list = self.parse_column_def_list()
        if column_list:
            node.add_child(column_list)
        else:
            return None
        
        # ')'
        if not self.consume(TokenType.PUNCTUATION, ')'):
            return None
        
        return node
    
    def parse_column_def_list(self):
        """
        Parse column definition list
        
        ColumnDefList -> ColumnDef (',' ColumnDef)*
        ColumnDef -> Identifier DataType
        """
        node = ParseTreeNode("COLUMN_DEF_LIST")
        
        column_def = self.parse_column_def()
        if column_def:
            node.add_child(column_def)
        else:
            return None
        
        while self.match(TokenType.PUNCTUATION, ','):
            self.advance()  # consume comma
            col_def = self.parse_column_def()
            if col_def:
                node.add_child(col_def)
            else:
                break
        
        return node
    
    def parse_column_def(self):
        """
        Parse a column definition
        
        ColumnDef -> Identifier DataType
        """
        node = ParseTreeNode("COLUMN_DEF")
        
        # Identifier
        identifier = self.parse_identifier()
        if identifier:
            node.add_child(identifier)
        else:
            return None
        
        # DataType
        data_type = self.parse_data_type()
        if data_type:
            node.add_child(data_type)
        else:
            return None
        
        return node
    
    def parse_data_type(self):
        """
        Parse data type
        
        DataType -> INT | FLOAT | TEXT
        """
        token = self.current_token()
        if token is None or token.type != TokenType.KEYWORD:
            line = token.line if token else 0
            col = token.column if token else 0
            self.report_error(
                f"Expected data type (INT, FLOAT, or TEXT) at line {line}, position {col}, but found {token.type.value if token else 'end of input'}",
                line, col
            )
            return None
        
        keyword = token.lexeme.upper()
        if keyword not in ['INT', 'FLOAT', 'TEXT']:
            self.report_error(
                f"Expected data type (INT, FLOAT, or TEXT) at line {token.line}, position {token.column}, but found '{keyword}'",
                token.line, token.column
            )
            return None
        
        node = ParseTreeNode("DATA_TYPE", keyword)
        node.set_position(token.line, token.column)
        self.advance()
        return node
    
    def parse_where_clause(self):
        """
        Parse WHERE clause
        
        WHERE_CLAUSE -> WHERE Condition
        """
        node = ParseTreeNode("WHERE_CLAUSE")
        start_token = self.current_token()
        node.set_position(start_token.line, start_token.column)
        
        # WHERE
        if not self.consume(TokenType.KEYWORD, 'WHERE'):
            return None
        
        # Condition
        condition = self.parse_condition()
        if condition:
            node.add_child(condition)
        else:
            return None
        
        return node
    
    def parse_condition(self):
        """
        Parse condition with AND, OR, NOT support
        
        Condition -> Condition OR ConditionTerm
                  | ConditionTerm
        ConditionTerm -> ConditionTerm AND ConditionFactor
                       | ConditionFactor
        ConditionFactor -> NOT ConditionFactor
                         | Comparison
                         | '(' Condition ')'
        """
        # Start with OR (lowest precedence)
        return self.parse_or_condition()
    
    def parse_or_condition(self):
        """
        Parse OR conditions (lowest precedence)
        
        Condition -> ConditionTerm (OR ConditionTerm)*
        """
        left = self.parse_and_condition()
        if left is None:
            return None
        
        node = left
        
        while self.match(TokenType.KEYWORD, 'OR'):
            or_token = self.current_token()
            self.advance()  # consume OR
            
            right = self.parse_and_condition()
            if right is None:
                break
            
            # Create OR node
            or_node = ParseTreeNode("OR_CONDITION")
            or_node.set_position(or_token.line, or_token.column)
            or_node.add_child(node)
            or_node.add_child(right)
            node = or_node
        
        return node
    
    def parse_and_condition(self):
        """
        Parse AND conditions (medium precedence)
        
        ConditionTerm -> ConditionFactor (AND ConditionFactor)*
        """
        left = self.parse_not_condition()
        if left is None:
            return None
        
        node = left
        
        while self.match(TokenType.KEYWORD, 'AND'):
            and_token = self.current_token()
            self.advance()  # consume AND
            
            right = self.parse_not_condition()
            if right is None:
                break
            
            # Create AND node
            and_node = ParseTreeNode("AND_CONDITION")
            and_node.set_position(and_token.line, and_token.column)
            and_node.add_child(node)
            and_node.add_child(right)
            node = and_node
        
        return node
    
    def parse_not_condition(self):
        """
        Parse NOT conditions and comparisons (highest precedence)
        
        ConditionFactor -> NOT ConditionFactor
                         | Comparison
                         | '(' Condition ')'
        """
        # NOT operator
        if self.match(TokenType.KEYWORD, 'NOT'):
            not_token = self.current_token()
            self.advance()  # consume NOT
            
            operand = self.parse_not_condition()  # Recursive for NOT NOT ...
            if operand is None:
                return None
            
            node = ParseTreeNode("NOT_CONDITION")
            node.set_position(not_token.line, not_token.column)
            node.add_child(operand)
            return node
        
        # Parenthesized condition
        if self.match(TokenType.PUNCTUATION, '('):
            self.advance()  # consume '('
            condition = self.parse_condition()
            if condition is None:
                return None
            
            if not self.consume(TokenType.PUNCTUATION, ')'):
                return None
            
            return condition
        
        # Comparison
        return self.parse_comparison()
    
    def parse_comparison(self):
        """
        Parse comparison expression
        
        Comparison -> Expression Operator Expression
                    | Identifier
        """
        node = ParseTreeNode("COMPARISON")
        
        # Left side
        left = self.parse_expression()
        if left is None:
            return None
        
        node.add_child(left)
        
        # Operator (if present)
        token = self.current_token()
        if token and token.type == TokenType.OPERATOR:
            operator = token.lexeme
            if operator in ['=', '!=', '<>', '<', '<=', '>', '>=']:
                op_node = ParseTreeNode("OPERATOR", operator)
                op_node.set_position(token.line, token.column)
                node.add_child(op_node)
                self.advance()
                
                # Right side
                right = self.parse_expression()
                if right:
                    node.add_child(right)
        else:
            # Just an identifier (for boolean columns)
            pass
        
        return node
    
    def parse_expression(self):
        """
        Parse arithmetic expression
        
        Expression -> Term (('+' | '-') Term)*
        """
        left = self.parse_term()
        if left is None:
            return None
        
        node = left
        
        while self.current_token():
            token = self.current_token()
            if token.type == TokenType.OPERATOR and token.lexeme in ['+', '-']:
                op_token = token
                self.advance()
                
                right = self.parse_term()
                if right is None:
                    break
                
                op_node = ParseTreeNode("EXPRESSION", op_token.lexeme)
                op_node.set_position(op_token.line, op_token.column)
                op_node.add_child(node)
                op_node.add_child(right)
                node = op_node
            else:
                break
        
        return node
    
    def parse_term(self):
        """
        Parse term (multiplication and division)
        
        Term -> Factor (('*' | '/' | '%') Factor)*
        """
        left = self.parse_factor()
        if left is None:
            return None
        
        node = left
        
        while self.current_token():
            token = self.current_token()
            if token.type == TokenType.OPERATOR and token.lexeme in ['*', '/', '%']:
                op_token = token
                self.advance()
                
                right = self.parse_factor()
                if right is None:
                    break
                
                op_node = ParseTreeNode("TERM", op_token.lexeme)
                op_node.set_position(op_token.line, op_token.column)
                op_node.add_child(node)
                op_node.add_child(right)
                node = op_node
            else:
                break
        
        return node
    
    def parse_factor(self):
        """
        Parse factor (base elements)
        
        Factor -> Identifier
                | Literal
                | '(' Expression ')'
        """
        token = self.current_token()
        if token is None:
            return None
        
        # Parenthesized expression
        if token.type == TokenType.PUNCTUATION and token.lexeme == '(':
            self.advance()  # consume '('
            expr = self.parse_expression()
            if expr is None:
                return None
            
            if not self.consume(TokenType.PUNCTUATION, ')'):
                return None
            
            return expr
        
        # Identifier
        if token.type == TokenType.IDENTIFIER:
            return self.parse_identifier()
        
        # Literal
        if token.type in [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.STRING_LITERAL]:
            node = ParseTreeNode("LITERAL", token.lexeme)
            node.set_position(token.line, token.column)
            self.advance()
            return node
        
        return None
    
    def parse_identifier(self):
        """
        Parse identifier
        
        Identifier -> IDENTIFIER token
        """
        token = self.current_token()
        if token is None:
            return None
        
        if token.type != TokenType.IDENTIFIER:
            return None
        
        node = ParseTreeNode("IDENTIFIER", token.lexeme)
        node.set_position(token.line, token.column)
        self.advance()
        return node
