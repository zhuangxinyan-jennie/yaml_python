#utf-8
#---utf-8---
from tree_sitter import Language,Parser
import tree_sitter_c

# ===== 初始化 Tree-sitter =====
try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    def get_parser():
        parser = Parser()
        parser.language = C_LANGUAGE
        return parser
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    def get_parser():
        parser = Parser()
        parser.set_language(C_LANGUAGE)
        return parser