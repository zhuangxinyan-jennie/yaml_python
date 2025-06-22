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



c_code = """

int max(int a, int b)
{
    return a > b ? a : b;
}   

int add(int a, int b)
{
    return a + b;
}

int sub(int a, int b)
{
    int c = max(a,b);

    return c - b;
}

void example (char *str, int i, float f)
{
    add(1,2);
    sub(1,2);
    return 0;
}
# example 是最顶层父函数

"""
#只要父函数
def interList(code):
    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node

    name_all_func = [] # 存储所有函数名
    name_called_all_func = []  #存储被调用函数名
    top_func = []
    interlist = []


    # top_func = []

    # name = []
    # interlist = []


    # 寻找父函数

# 先把所有函数名和被调用函数名存储起来
    for node_find_all_func in root_node.children:
        if node_find_all_func.type == "function_definition": # 找到函数

            # name_all_func = [] # 存储所有函数名
            # name_called_all_func = []  #存储被调用函数名
            # # interlist= [] #找到函数
            for node2 in node_find_all_func.children:
                if node2.type == "function_declarator": # 找到函数名字
                    name_all_func.append(node2.children[0].text.decode('utf-8'))

        # 到此找到所有被调用函数名



            cursor = node_find_all_func.walk()
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
            
            #采用DFS遍历  子 兄弟 父


            # for node3 in node_find_all_func.children:
            #     if node3.type == "compound_statement":
            #         for call_find in node3.children:
            #             if call_find.type == "expression_statement":
            #                 for call_find2 in call_find.children:
            #                     if call_find2.type == "call_expression":
            #                         name_called_all_func.append(call_find2.children[0].text.decode('utf-8'))
            #                         # 获取参数声明的最后一个子节点（变量名）
                                    # var_name = call_find.children[-1].text.decode('utf-8')
    # print(name_all_func) # type: ignore
    # print(name_called_all_func) # type: ignore

    #定义顶层函数
    for topname in name_all_func:
        if topname not in name_called_all_func:
            top_func.append(topname)
    #print(top_func) # type: ignore


    # 第二次遍历
    # for find_top_func in root_node.children:

    cursor_find_top_func = root_node.walk()
    top_func_reached_end = False
            
    while not top_func_reached_end:
            if cursor_find_top_func.node.type == "function_definition":
                for node4 in cursor_find_top_func.node.children:
                    if node4.type == "function_declarator":
                        func_name = node4.children[0].text.decode('utf-8')
                        if func_name in top_func:
                            for node5 in node4.children:
                                if node5.type == "parameter_list":
                                    for node6 in node5.children:
                                        if node6.type == "parameter_declaration":
                                            interlist.append(node6.children[-1].text.decode('utf-8'))

                # 移动到下一个节点
            if cursor_find_top_func.goto_first_child():
                    continue
                
            if cursor_find_top_func.goto_next_sibling():
                    continue
                
            while not cursor_find_top_func.goto_next_sibling():
                if not cursor_find_top_func.goto_parent():
                    top_func_reached_end = True
                    break

# top_func = name_all_func-name_called_all_func
            # print(f"- {name} {interlist}") # type: ignore
            # for param in interlist:
            #     print(f"- {name} {param}")
    print("interList:")

    for i in interlist: # type: ignore
        print(f"    - {top_func[0]} {i}")

# interList(c_code)
    return interlist









