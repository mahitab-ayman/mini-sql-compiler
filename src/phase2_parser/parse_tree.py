"""
Parse Tree Node Structure for SQL-like Language
Represents the hierarchical derivation of token sequences using grammar rules
"""


class ParseTreeNode:
    """Represents a node in the parse tree"""
    
    def __init__(self, node_type, value=None, children=None):
        """
        Initialize a parse tree node
        
        Args:
            node_type: The type/category of the node (e.g., 'SELECT_STMT', 'CONDITION', 'EXPRESSION')
            value: The value/lexeme associated with this node (for leaf nodes)
            children: List of child nodes
        """
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []
        self.line = None
        self.column = None
    
    def add_child(self, child):
        """Add a child node"""
        if child is not None:
            self.children.append(child)
    
    def set_position(self, line, column):
        """Set the line and column position for this node"""
        self.line = line
        self.column = column
    
    def __repr__(self):
        """String representation of the node"""
        if self.value is not None:
            return f"{self.node_type}({self.value})"
        return f"{self.node_type}[{len(self.children)} children]"
    
    def to_string(self, indent=0):
        """Convert the tree to a formatted string representation"""
        prefix = "  " * indent
        result = f"{prefix}{self.node_type}"
        
        if self.value is not None:
            result += f": {self.value}"
        
        if self.line is not None and self.column is not None:
            result += f" [Line: {self.line}, Col: {self.column}]"
        
        result += "\n"
        
        for child in self.children:
            result += child.to_string(indent + 1)
        
        return result
    
    def __str__(self):
        return self.to_string()

