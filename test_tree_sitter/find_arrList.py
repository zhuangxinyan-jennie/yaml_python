#utf-8
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




int main() {
    int arr[10] = {1,2,3,4,5,6,7,8,9,10};
    for (int i = 0; i < 10; i++) {
        printf("%d\n", arr[i]);
    }
    return 0;
}


"""
#只要父函数
def find_arrList(code):
    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node

    name_all_func = [] 
    name_called_all_func = []  
    top_func = []
    arrlist = []

    # 第一次遍历：找出所有函数和被调用函数
    for node_find_all_func in root_node.children:
        if node_find_all_func.type == "function_definition":
            for node2 in node_find_all_func.children:
                if node2.type == "function_declarator":
                    func_name = node2.children[0].text.decode('utf-8')
                    print(f"Found function: {func_name}")  # 调试输出1
                    name_all_func.append(func_name)

            cursor = node_find_all_func.walk()
            reached_end = False
            while not reached_end:
                if cursor.node.type == "call_expression":
                    called_func = cursor.node.children[0].text.decode('utf-8')
                    print(f"Found called function: {called_func}")  # 调试输出2
                    name_called_all_func.append(called_func)

                if cursor.goto_first_child():
                    continue
                if cursor.goto_next_sibling():
                    continue
                while not cursor.goto_next_sibling():
                    if not cursor.goto_parent():
                        reached_end = True
                        break

    # 找出顶层函数
    for topname in name_all_func:
        if topname not in name_called_all_func:
            print(f"Found top function: {topname}")  # 调试输出3
            top_func.append(topname)

    # 第二次遍历：在顶层函数中找数组
    for node_find_all_func in root_node.children:
        if node_find_all_func.type == "function_definition":
            for node2 in node_find_all_func.children:
                if node2.type == "function_declarator":
                    func_name = node2.children[0].text.decode('utf-8')
                    if func_name in top_func:  # 是顶层函数
                        for compound in node_find_all_func.children:
                            if compound.type == "compound_statement":
                                for decl in compound.children:
                                    if decl.type == "declaration":
                                        # 遍历声明的子节点
                                        for init_decl in decl.children:
                                            if init_decl.type == "init_declarator":
                                                # 检查第一个子节点是否是数组声明
                                                first_child = init_decl.children[0]
                                                if first_child.type == "array_declarator":
                                                    # 获取数组名
                                                    arr_name = first_child.children[0].text.decode('utf-8')
                                                    # print(f"Found array: {arr_name}")
                                                    arrlist.append(arr_name)

    # print(f"Final arrlist: {arrlist}")
    return arrlist
# find_arrList(c_code)









