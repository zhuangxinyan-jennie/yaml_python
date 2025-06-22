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

# ===== 自动检测顶层函数（最外层调用者） =====
def detect_top_function_via_call_graph(root_node, source_code):
    calls = {}
    defined_functions = set()

    # def traverse(n, current_func=None):
    #     if n.type == 'function_definition':
    #         declarator = n.child_by_field_name('declarator')
    #         func_id = None
    #         for child in declarator.children:
    #             if child.type == 'identifier':
    #                 func_id = child
    #                 break
    #         if func_id:
    #             current_func = source_code[func_id.start_byte:func_id.end_byte]
    #             defined_functions.add(current_func)
    #             calls.setdefault(current_func, set())

    #     if n.type == 'call_expression':
    #         func_node = n.child_by_field_name('function')
    #         if func_node and func_node.type == 'identifier':
    #             callee = source_code[func_node.start_byte:func_node.end_byte]
    #             if current_func:
    #                 calls.setdefault(current_func, set()).add(callee)

    #     for child in n.children:
    #         traverse(child, current_func)

    # traverse(root_node)

    # all_callees = {callee for callees in calls.values() for callee in callees}
    # top_funcs = [func for func in calls if func not in all_callees]
    # top_func = max(top_funcs, key=len) if top_funcs else None
    # return top_func, calls


    def extract_identifier_from_declarator(declarator_node):
        stack = [declarator_node]
        while stack:
            node = stack.pop()
            if node.type == 'identifier':
                return source_code[node.start_byte:node.end_byte]
            stack.extend(reversed(node.children))
        return None

    def traverse(n, current_func=None):
        nonlocal calls, defined_functions
        if n.type == 'function_definition':
            declarator = n.child_by_field_name('declarator')
            func_name = extract_identifier_from_declarator(declarator) if declarator else None
            if func_name:
                current_func = func_name
                defined_functions.add(current_func)
                calls.setdefault(current_func, set())

        elif n.type == 'call_expression':
            func_node = n.child_by_field_name('function')
            if func_node and func_node.type == 'identifier':
                callee = source_code[func_node.start_byte:func_node.end_byte]
                if current_func:
                    calls.setdefault(current_func, set()).add(callee)

        for child in n.children:
            traverse(child, current_func)

    traverse(root_node)

    all_callees = {callee for callees in calls.values() for callee in callees}
    top_funcs = [func for func in calls if func not in all_callees]

    if 'main' in top_funcs:
        top_func = 'main'
    elif top_funcs:
        top_func = sorted(top_funcs)[0]
    else:
        top_func = None

    return top_func, calls