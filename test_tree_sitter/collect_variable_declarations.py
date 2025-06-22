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

# ===== 收集变量声明 =====
def collect_variable_declarations(main_func_node, source_code, macro_map):
    variables = {}
    
    def extract_declarator(node):
        """深度遍历提取变量名"""
        stack = [node]
        while stack:
            current = stack.pop()
            if current.type == 'identifier':
                return [source_code[current.start_byte:current.end_byte]]
            stack.extend(reversed(current.children))
        return []
    
    def traverse(n):
        if n.type == 'declaration':
            # 提取类型节点（处理 TYPE 宏）
            type_node = next((
                child for child in n.children 
                if child.type in ('primitive_type', 'type_identifier')
            ), None)
            if not type_node:
                return
            
            # 动态解析宏定义
            raw_type = source_code[type_node.start_byte:type_node.end_byte]
            resolved_type = macro_map.get(raw_type, raw_type)
            final_type = resolved_type.lower()  # 统一转为小写
            
            # 提取所有声明符（支持未初始化声明）
            declarators = []
            for child in n.children:
                if child.type == 'declarator':
                    var_name = extract_declarator(child)
                    if var_name:
                        declarators.extend(var_name)
                elif child.type == 'init_declarator':
                    declarator_part = child.child_by_field_name('declarator')
                    var_name = extract_declarator(declarator_part)
                    if var_name:
                        declarators.extend(var_name)
            
            # 记录变量类型
            for var in declarators:
                variables[var] = final_type
                print(f"[DEBUG] 变量声明: {var} => {final_type}")
        
        for child in n.children:
            traverse(child)
    
    traverse(main_func_node)
    return variables