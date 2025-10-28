class SymbolTable:
    def __init__(self):
        self.table = {}

    def add(self, identifier, line, column):
        if identifier not in self.table:
            self.table[identifier] = {
                "first_line": line,
                "first_column": column,
                "occurrences": 1
            }
        else:
            self.table[identifier]["occurrences"] += 1

    def get(self, identifier):
        return self.table.get(identifier)

    def all_symbols(self):
        return self.table
