class ErrorHandler:
    def __init__(self):
        self.errors = []

    def add_error(self, line, col, message):
        self.errors.append({
            "line": line,
            "column": col,
            "message": message
        })

    def has_errors(self):
        return len(self.errors) > 0

    def display_errors(self):
        for e in self.errors:
            print(f"Error: {e['message']} at line {e['line']}, column {e['column']}.")
