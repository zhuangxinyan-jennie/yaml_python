# -*- coding: utf-8 -*-
from tree_sitter import Language, Parser
import tree_sitter_c

# 初始化 Tree-sitter
try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)

# 读取 C 文件
with open('aes.c', 'r', encoding='utf-8') as f:
    code = f.read()

# 解析代码
tree = parser.parse(bytes(code, 'utf8'))
root_node = tree.root_node

# 打印所有定义的函数
print("Functions defined:")
for node in root_node.children:
    if node.type == "function_definition":
        # 打印函数名
        for child in node.children:
            if child.type == "function_declarator":
                func_name = child.children[0].text.decode('utf-8')
                print(f"  Function name: {func_name}")
                
                # 检查是否是 aes_mixColumns
                if func_name == "aes_mixColumns":
                    print("    Found aes_mixColumns function!")
                    # 打印函数体的结构
                    for body_child in node.children:
                        if body_child.type == "compound_statement":
                            print("    Function body structure:")
                            for stmt in body_child.children:
                                print(f"      Statement type: {stmt.type}")
                                if stmt.type == "expression_statement":
                                    for expr in stmt.children:
                                        print(f"        Expression type: {expr.type}")
                                        if expr.type == "call_expression":
                                            for arg in expr.children:
                                                print(f"          Argument type: {arg.type}")

# 打印所有函数调用
print("\nFunction calls:")
cursor = root_node.walk()
reached_end = False

while not reached_end:
    if cursor.node.type == "call_expression":
        func_name = cursor.node.children[0].text.decode('utf-8')
        print(f"  Called function: {func_name}")
        
        # 打印调用上下文
        parent = cursor.node.parent
        if parent:
            print(f"    Call context: {parent.type}")
            if parent.type == "expression_statement":
                print("      In expression statement")
            elif parent.type == "declaration":
                print("      In declaration statement")
    
    # 移动到下一个节点
    if cursor.goto_first_child():
        continue
    
    if cursor.goto_next_sibling():
        continue
    
    while not cursor.goto_next_sibling():
        if not cursor.goto_parent():
            reached_end = True
            break 