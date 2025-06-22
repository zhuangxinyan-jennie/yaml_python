#---utf-8---
from tree_sitter import Language,Parser
import tree_sitter_c
import os
from parse_header_macros import parse_header_macros
try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)
    
# ===== 提取指定前缀的函数调用 =====
def extract_function_calls(node, source_code, file_prefix='aes'):
    target_prefix = file_prefix
    calls = set()

    # === 新增的代码开始 ===
    macro_map = parse_header_macros(os.path.abspath(source_code), source_code)

    # def traverse(n):
    #     if n.type == 'call_expression':
    #         func_node = n.child_by_field_name('function')
    #         if func_node and func_node.type == 'identifier':
    #             func_name = source_code[func_node.start_byte:func_node.end_byte]
    #             if func_name.startswith(target_prefix):
    #                 calls.add(func_name)
    def traverse(n):
        if n.type == 'call_expression':
            # 检查函数调用
            func_node = n.child_by_field_name('function')
            if func_node and func_node.type == 'identifier':
                func_name = source_code[func_node.start_byte:func_node.end_byte]
                if func_name.startswith(target_prefix):
                    calls.add(func_name)
        elif n.type == 'identifier':
            # 检查所有宏的使用
            identifier_name = source_code[n.start_byte:n.end_byte]
            if identifier_name in macro_map:
                calls.add(identifier_name)

 

        for child in n.children:
            traverse(child)

    traverse(node)
    return sorted(calls)