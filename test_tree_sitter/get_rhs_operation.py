#---utf-8---
from tree_sitter import Language,Parser
import tree_sitter_c

try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)


# ===== 收集赋值操作 =====
def get_rhs_operation(node, source_code):
    """深度优先遍历右值表达式，识别主运算符"""
    if node.type == 'binary_expression':
        operator = source_code[node.child_by_field_name('operator').start_byte:node.child_by_field_name('operator').end_byte]
        return {'*': 'mul', '+': 'add', '-': 'sub'}.get(operator, None)
    # 
    for child in node.children:
        result = get_rhs_operation(child, source_code)
        if result:
            return result
    return None