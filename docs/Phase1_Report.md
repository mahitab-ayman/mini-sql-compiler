# Mini SQL Compiler — Lexical Analysis (Phase 1)

## Brief Report

### Team Members
- **Nada Zaki** — ID: 221000829 — Email: n.gamal2229@nu.edu.eg  
- **Mona Elsayed** — ID: 221000415 — Email: m.gomaa2215@nu.edu.eg  
- **Mahitab Ayman** — ID: 212002434 — Email: m.ayman2134@nu.edu.eg  

---

## 1. Introduction
This phase focuses on the **Lexical Analysis** stage of the Mini SQL Compiler project.  
The objective is to design a lexical analyzer that reads SQL-like input, identifies valid tokens, classifies them according to predefined rules, and detects invalid patterns.  
The lexer also removes comments and whitespace while reporting any lexical errors.

---

## 2. Tokens Implemented
The lexer recognizes and categorizes the following token types using Python’s `Enum` class for clarity and maintainability.

| Token Type | Description |
|-------------|-------------|
| **KEYWORD** | SQL reserved words such as `SELECT`, `FROM`, `WHERE`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `TABLE`, `INT`, `FLOAT`, `TEXT`, `AND`, `OR`, `NOT`. |
| **IDENTIFIER** | User-defined names following the pattern `[a-zA-Z_][a-zA-Z0-9_]*`. |
| **INT_LITERAL** | Integer constants such as `10`, `25`, etc. |
| **FLOAT_LITERAL** | Floating-point constants such as `3.14`, `45.6`, etc. |
| **STRING_LITERAL** | Text enclosed in single quotes `'example'`. |
| **OPERATOR** | Arithmetic and relational operators like `+`, `-`, `*`, `/`, `=`, `!=`, `<`, `<=`, `>`, `>=`. |
| **PUNCTUATION** | Symbols such as `,`, `;`, `(`, `)`. |
| **COMMENT** | Single-line (`-- comment`) and multi-line (`/* ... */`) comments. |
| **EOF** | Indicates the end of file. |
| **ERROR** | Represents invalid or unrecognized symbols. |

The tokens are grouped into predefined sets:
- `KEYWORDS`
- `OPERATORS`
- `DELIMITERS`

---

## 3. Error Handling
Error handling is managed by the **ErrorHandler** class, which records lexical errors during tokenization.  
When the lexer encounters an invalid character, unterminated string, or malformed token, it uses the `add_error()` method:

```python
def add_error(self, message, line=None, column=None):
    self.errors.append({
        "message": message,
        "line": line,
        "column": column
    })
```

At the end of the analysis:
- **`has_errors()`** checks if any errors occurred.  
- **`get_errors()`** retrieves all recorded errors for display.  

This design allows the lexer to continue scanning after errors and provides detailed feedback with precise line and column locations.

---

## 4. Challenges and Solutions

### a. Overlapping Patterns
- **Issue:** Operators like `<`, `<=`, `!=` conflicted in matching order.  
- **Solution:** Checked multi-character operators before single-character ones.

### b. Skipping Comments and Whitespace
- **Issue:** Comments and spaces were initially tokenized.  
- **Solution:** Filtered them out before final token generation.

### c. Invalid Token Detection
- **Issue:** Illegal symbols (e.g., `@abc`, `1var`) weren’t handled.  
- **Solution:** Added a fallback case for `ERROR` tokens and logged them via `ErrorHandler`.

### d. Token Order Preservation
- **Issue:** Tokens appeared in the wrong order.  
- **Solution:** Used an index tracker (`pos`) to advance only after confirming a match.

### e. String Literal Issues
- **Issue:** Unterminated or escaped strings caused parsing problems.  
- **Solution:** Used a non-greedy regex `' (.*?) '` and added error reporting for missing quotes.

---

## 5. Conclusion
The **Lexical Analysis** phase successfully converts SQL-like input into structured tokens while identifying invalid patterns.  
It provides a solid foundation for syntax and semantic analysis, with reliable error detection and consistent token management.  
This marks a strong start for building the remaining compiler phases efficiently and accurately.
