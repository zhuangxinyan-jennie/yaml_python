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

def generate_dict_op(top_func, variables, assignments):
    dict_op = {t: {} for t in ('int', 'float', 'double', 'half')}
    type_map = {
        'int': ('int', ''),
        'float': ('float', 'f'),
        'double': ('double', 'd'),
        'half': ('half', 'h')
    }
    
    for var_name, op_type, loop_label in assignments:
        if not var_name:
            print(f"[WARN] 跳过变量名为空的赋值: {op_type}, 循环标签: {loop_label}")
            continue
        if not loop_label or loop_label.strip() == '':
            print(f"[WARN] 跳过无效循环标签的变量: {var_name}")
            continue
        
        # 类型推断逻辑（修复大小写敏感问题）
        var_type = variables.get(var_name, 'int').lower()
        target_type = 'int'
        prefix = ''
        for base_type in ['half', 'double', 'float']:
            if var_type == base_type:
                target_type = base_type
                prefix = type_map[base_type][1]
                break
        
        # 生成操作符和循环路径
        full_op = f"{prefix}{op_type}" if prefix else op_type
        loop_path = f"{top_func}/{loop_label}"
        dict_key = f"{loop_path} {var_name}"
        
        # 更新字典
        dict_op[target_type].setdefault(dict_key, []).append(full_op)
    
    # 清理空条目
    for type_key in list(dict_op.keys()):
        entries = dict_op[type_key]
        filtered = [{k: sorted(list(set(v)))} for k, v in entries.items() if v]
        dict_op[type_key] = filtered
        if not filtered:
            del dict_op[type_key]
    
    return dict_op