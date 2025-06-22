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


# 0410 改动 筛选函数名，不要选入printf之类的

#只要父函数
def funcList(code):
    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node

    name_all_func = [] # 存储所有函数名
    name_called_all_func = []  #存储被调用函数名
    top_func = []
    funclist_final = []

    # 先把所有函数名存储起来
    for node_find_all_func in root_node.children:
        if node_find_all_func.type == "function_definition":
            for node2 in node_find_all_func.children:
                if node2.type == "function_declarator":
                    name_all_func.append(node2.children[0].text.decode('utf-8'))

    # 找到所有被调用的函数名
    cursor = root_node.walk()
    reached_end = False
            
    while not reached_end:
        if cursor.node.type == "call_expression":
            name_called_all_func.append(cursor.node.children[0].text.decode('utf-8'))

        # 移动到下一个节点
        if cursor.goto_first_child():
            continue
                
        if cursor.goto_next_sibling():
            continue
                
        while not cursor.goto_next_sibling():
            if not cursor.goto_parent():
                reached_end = True
                break

    # 定义顶层函数
    for topname in name_all_func:
        if topname not in name_called_all_func:
            top_func.append(topname)

    # 查找在顶层函数中被调用的函数
    cursor_find_top_func = root_node.walk()
    top_func_reached_end = False
            
    while not top_func_reached_end:
        if cursor_find_top_func.node.type == "function_definition":
            # 检查是否是顶层函数
            for node4 in cursor_find_top_func.node.children:
                if node4.type == "function_declarator":
                    func_name = node4.children[0].text.decode('utf-8')
                    if func_name in top_func:
                        # 使用游标遍历顶层函数中的所有表达式
                        #=============================================================0411#
                        func_cursor = cursor_find_top_func.node.walk()
                        func_reached_end = False
                        
                        while not func_reached_end:
                            if func_cursor.node.type == "call_expression":
                                called_func = func_cursor.node.children[0].text.decode('utf-8')
                                if called_func in name_all_func:  # 只添加在代码中定义的函数
                                    funclist_final.append(called_func)
                            
                            # 移动到下一个节点
                            if func_cursor.goto_first_child():
                                continue
                                
                            if func_cursor.goto_next_sibling():
                                continue
                                
                            while not func_cursor.goto_next_sibling():
                                if not func_cursor.goto_parent():
                                    func_reached_end = True
                                    break

        # 移动到下一个节点
        if cursor_find_top_func.goto_first_child():
            continue
                
        if cursor_find_top_func.goto_next_sibling():
            continue
                
        while not cursor_find_top_func.goto_next_sibling():
            if not cursor_find_top_func.goto_parent():
                top_func_reached_end = True
                break

    return sorted(list(set(funclist_final)))  









