import tree_sitter
import tree_sitter_c
import sys

print("Python 版本:", sys.version)
print("tree-sitter 版本:", tree_sitter.__version__)
print("tree-sitter-c 版本:", getattr(tree_sitter_c, '__version__', '未知'))