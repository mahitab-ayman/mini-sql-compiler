# Mini SQL Compiler — Phase 2: Syntax Analysis Report

## Team Members
- **Nada Zaki** — ID: 221000829 — Email: n.gamal2229@nu.edu.eg  
- **Mona Elsayed** — ID: 221000415 — Email: m.gomaa2215@nu.edu.eg  
- **Mahitab Ayman** — ID: 212002434 — Email: m.ayman2134@nu.edu.eg

---

## 1. Formal Grammar (EBNF Notation)

```
Program -> Statement (';' Statement)* ';'?

Statement -> SELECT_STMT | INSERT_STMT | UPDATE_STMT | DELETE_STMT | CREATE_STMT

-- SELECT Statement
SELECT_STMT -> SELECT SelectList FROM Identifier [WHERE Condition]
SelectList -> '*' | ColumnList
ColumnList -> SelectItem (',' SelectItem)*
SelectItem -> Identifier | Expression

-- INSERT Statement
INSERT_STMT -> INSERT INTO Identifier VALUES '(' ValueList ')'
ValueList -> Value (',' Value)*
Value -> Literal | Expression

-- UPDATE Statement
UPDATE_STMT -> UPDATE Identifier SET AssignmentList [WHERE Condition]
AssignmentList -> Assignment (',' Assignment)*
Assignment -> Identifier '=' Value

-- DELETE Statement
DELETE_STMT -> DELETE FROM Identifier [WHERE Condition]

-- CREATE TABLE Statement
CREATE_STMT -> CREATE TABLE Identifier '(' ColumnDefList ')'
ColumnDefList -> ColumnDef (',' ColumnDef)*
ColumnDef -> Identifier DataType
DataType -> INT | FLOAT | TEXT

-- WHERE Clause and Conditions
WHERE_CLAUSE -> WHERE Condition
Condition -> Condition OR ConditionTerm | ConditionTerm
ConditionTerm -> ConditionTerm AND ConditionFactor | ConditionFactor
ConditionFactor -> NOT ConditionFactor | Comparison | '(' Condition ')'
Comparison -> Expression Operator Expression | Identifier
Operator -> '=' | '!=' | '<>' | '<' | '<=' | '>' | '>='

-- Expressions
Expression -> Term (('+' | '-') Term)*
Term -> Factor (('*' | '/' | '%') Factor)*
Factor -> Identifier | Literal | '(' Expression ')'

-- Base Elements
Identifier -> [a-zA-Z_][a-zA-Z0-9_]*
Literal -> INT_LITERAL | FLOAT_LITERAL | STRING_LITERAL
```

**Operator Precedence** (highest to lowest): NOT → AND → OR → *, /, % → +, - → Comparison operators

---

## 2. Parsing Technique: Recursive Descent Parsing

**Choice and Justification:**

We implemented **Recursive Descent Parsing** for the following reasons:

1. **Simplicity**: Direct mapping of grammar rules to functions makes the code intuitive and maintainable
2. **No External Dependencies**: Built from scratch without parsing generator libraries (Yacc, Bison, Antlr) as required
3. **Precise Error Handling**: Allows detailed error reporting at specific parsing points
4. **Top-Down Approach**: Naturally follows grammar structure from statements down to base elements

**Implementation:**

The parser is implemented as a `SyntaxAnalyzer` class with recursive methods for each grammar rule:
- `parse_statement()` - Entry point for parsing statements
- `parse_select_statement()`, `parse_insert_statement()`, etc. - Statement parsers
- `parse_condition()` - Handles compound boolean queries with AND, OR, NOT
- `parse_expression()`, `parse_term()`, `parse_factor()` - Arithmetic expression parsing

---

## 3. Parse Tree Structure

**Node Class Hierarchy:**

The parse tree is represented using a `ParseTreeNode` class:

```python
class ParseTreeNode:
    - node_type: Type/category (e.g., 'SELECT_STMT', 'CONDITION', 'EXPRESSION')
    - value: Lexeme value for leaf nodes
    - children: List of child nodes
    - line, column: Position information for error reporting
```

**Tree Structure Example:**

For query: `SELECT name, age FROM Students WHERE age > 18 AND status = 'active';`

```
PROGRAM
└── SELECT_STMT [Line: 1, Col: 1]
    ├── SELECT_LIST
    │   ├── IDENTIFIER: name
    │   └── IDENTIFIER: age
    ├── IDENTIFIER: Students
    └── WHERE_CLAUSE
        └── AND_CONDITION
            ├── COMPARISON (age > 18)
            └── COMPARISON (status = 'active')
```

**Node Types:** Statement types (`SELECT_STMT`, `INSERT_STMT`, etc.), clause types (`WHERE_CLAUSE`, `SELECT_LIST`), condition types (`OR_CONDITION`, `AND_CONDITION`, `NOT_CONDITION`), expression types (`EXPRESSION`, `TERM`), and base types (`IDENTIFIER`, `LITERAL`, `OPERATOR`).

---

## 4. Syntax Error Detection and Error Recovery

**Error Detection:**

The parser detects syntax errors in the following scenarios:
1. **Missing Tokens**: Expected token not found (e.g., missing `FROM` keyword)
2. **Unexpected Tokens**: Token found where it shouldn't be (e.g., unexpected comma)
3. **Wrong Token Type**: Type mismatch (e.g., expecting IDENTIFIER but finding KEYWORD)
4. **Wrong Lexeme**: Token type matches but lexeme is incorrect

**Error Reporting Format:**

All syntax errors are reported with:
- **Line Number** and **Column Number** (derived from the token)
- **Descriptive Message** indicating what was expected versus what was found

**Example Error Message:**
```
Syntax Error: Expected 'FROM' at line 5, position 12, but found 'WHERE'.
```

**Implementation:**

The `consume()` method checks if the current token matches expectations. If not, it calls `report_error()` with detailed information. Errors are stored in an `ErrorHandler` object.

**Error Recovery Mechanism (Panic Mode):**

We implemented **panic mode** error recovery to enable detection of multiple errors in a single run:

1. **Synchronizing Tokens**: `;` (semicolon), `CREATE`, `SELECT`, `INSERT`, `UPDATE`, `DELETE`
2. **Recovery Algorithm**: The `synchronize()` method skips tokens until finding a synchronizing token, then resumes normal parsing
3. **Multiple Error Detection**: The parser continues parsing subsequent statements after an error, allowing all errors to be detected

**Example:**
For input with multiple errors:
```sql
SELECT name FROM Students WHERE;  -- Missing condition
INSERT INTO Users VALUES (1, 'John';  -- Missing closing parenthesis
UPDATE Users SET name = 'Jane';  -- Valid statement
```

The parser will report errors for the first two statements and successfully parse the third.

---

## Files Structure

```
src/phase2_parser/
├── __init__.py          # Module initialization
├── parser.py            # SyntaxAnalyzer class (Recursive Descent Parser)
├── parse_tree.py         # ParseTreeNode class definition
└── grammar.txt           # Complete formal grammar documentation
```

---

**End of Phase 2 Report**
