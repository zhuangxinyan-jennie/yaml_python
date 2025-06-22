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

#ֻҪ������
def find_top_func(code):
    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node

    name_all_func = [] # �洢���к�����
    name_called_all_func = []  #�洢�����ú�����
    top_func = []
    interlist = []


    # top_func = []

    # name = []
    # interlist = []


    # Ѱ�Ҹ�����

# �Ȱ����к������ͱ����ú������洢����
    for node_find_all_func in root_node.children:
        if node_find_all_func.type == "function_definition": # �ҵ�����

            # name_all_func = [] # �洢���к�����
            # name_called_all_func = []  #�洢�����ú�����
            # # interlist= [] #�ҵ�����
            for node2 in node_find_all_func.children:
                if node2.type == "function_declarator": # �ҵ���������
                    name_all_func.append(node2.children[0].text.decode('utf-8'))

        # �����ҵ����б����ú�����



            cursor = node_find_all_func.walk()
            reached_end = False
            
            while not reached_end:
                if cursor.node.type == "call_expression":
                    name_called_all_func.append(cursor.node.children[0].text.decode('utf-8'))

                # �ƶ�����һ���ڵ�
                if cursor.goto_first_child():
                    continue
                
                if cursor.goto_next_sibling():
                    continue
                
                while not cursor.goto_next_sibling():
                    if not cursor.goto_parent():
                        reached_end = True
                        break
            
            #����DFS����  �� �ֵ� ��


            # for node3 in node_find_all_func.children:
            #     if node3.type == "compound_statement":
            #         for call_find in node3.children:
            #             if call_find.type == "expression_statement":
            #                 for call_find2 in call_find.children:
            #                     if call_find2.type == "call_expression":
            #                         name_called_all_func.append(call_find2.children[0].text.decode('utf-8'))
            #                         # ��ȡ�������������һ���ӽڵ㣨��������
                                    # var_name = call_find.children[-1].text.decode('utf-8')
    # print(name_all_func) # type: ignore
    # print(name_called_all_func) # type: ignore

    #���嶥�㺯��
    for topname in name_all_func:
        if topname not in name_called_all_func:
            top_func.append(topname)
    #print(top_func) # type: ignore


    # �ڶ��α���
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

                # �ƶ�����һ���ڵ�
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
    # print("interList:")

    # for i in interlist: # type: ignore
    #     print(f"    - {top_func[0]} {i}")

# interList(c_code)
    return top_func









