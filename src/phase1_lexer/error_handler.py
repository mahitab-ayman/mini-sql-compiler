class ErrorHandler:
    def __init__(self):
        self.errors = []

    def add_error(self, message, line=None, column=None):
        self.errors.append({
            "message": message,
            "line": line,
            "column": column
        })

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors
