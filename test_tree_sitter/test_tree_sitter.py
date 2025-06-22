# -*- coding: utf-8 -*-
from tree_sitter import Language, Parser
import tree_sitter_python as tspython

# Initialize language
PY_LANGUAGE = Language(tspython.language())

# Create parser
parser = Parser()
parser.set_language(PY_LANGUAGE)

# Test code
python_code = """
def hello_world():
    print("Hello, Tree-sitter!")
    return 42
"""

# Parse code
tree = parser.parse(bytes(python_code, 'utf8'))

# Get root node
root_node = tree.root_node

# Print syntax tree
print("Syntax Tree Structure:")
print(root_node.sexp())

# Traverse all nodes
print("\nTraversing all nodes:")
def print_tree(node, level=0):
    print("  " * level + f"- {node.type}: {node.text.decode('utf8')}")
    for child in node.children:
        print_tree(child, level + 1)

print_tree(root_node) 