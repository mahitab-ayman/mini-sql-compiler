class ErrorHandler:
    def __init__(self):
        self.errors = []

    def add_error(self, message, line, column=None):
        if column:
            self.errors.append(f"Error: {message} at line {line}, column {column}")
        else:
            self.errors.append(f"Error: {message} at line {line}")

    def has_errors(self):
        return len(self.errors) > 0

    def display_errors(self):
        if self.errors:
            print("\nErrors Detected:")
            print("-" * 40)
            for err in self.errors:
                print(err)
            print("-" * 40)
        else:
            print("No Errors Detected")
