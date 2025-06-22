#---utf-8---
from tree_sitter import Language,Parser
import tree_sitter_c
from get_rhs_operation import get_rhs_operation

try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)

# ===== 收集赋值操作 =====



def collect_assignments(main_func_node, source_code, loops):
    assignments = []
    
    # 递归收集所有循环（含嵌套）
    all_loops = []
    def collect_loops(loop_list):
        for loop in loop_list:
            all_loops.append(loop)
            collect_loops(loop.get('inner_loops', []))
    collect_loops(loops)
    all_loops.sort(key=lambda x: (-x['start_byte'], x['end_byte']))  # 内层循环优先
    
    def traverse(n):
        # 处理赋值表达式（含复合赋值）
        if n.type == 'assignment_expression':
            left = n.child_by_field_name('left')
            operator = n.child_by_field_name('operator')
            right = n.child_by_field_name('right')
            
            if not (left and operator and right):
                return
                
            var_name = source_code[left.start_byte:left.end_byte] if left.type == 'identifier' else None
            op = source_code[operator.start_byte:operator.end_byte]
            
            # ȷ����������
            if op == '=':
                rhs_op = get_rhs_operation(right, source_code)
                op_type = rhs_op or 'assign'
            else:
                op_type = {'+=': 'add', '-=': 'sub', '*=': 'mul'}.get(op, None)
            
            if op_type == 'assign' or not op_type:
                return
                
            # ��λѭ����ǩ
            current_byte = n.start_byte
            selected_loop = next(
                (loop for loop in all_loops 
                 if loop['start_byte'] <= current_byte <= loop['end_byte']),
                None
            )
            loop_label = selected_loop['label'] if selected_loop else None
            
            assignments.append( (var_name, op_type, loop_label) )
        
        # 处理自增/自减操作（i++, j--）
        elif n.type == 'update_expression':
            operator = source_code[n.start_byte:n.end_byte]
            operand = n.child_by_field_name('argument')
            if operand and operand.type == 'identifier':
                var_name = source_code[operand.start_byte:operand.end_byte]
                op_type = 'add' if '++' in operator else 'sub'
                
                # 定位循环标签
                current_byte = n.start_byte
                selected_loop = next(
                    (loop for loop in all_loops 
                     if loop['start_byte'] <= current_byte <= loop['end_byte']),
                    None
                )
                loop_label = selected_loop['label'] if selected_loop else None
                
                if var_name and op_type != 'assign':
                    assignments.append((var_name, op_type, loop_label))
        
        for child in n.children:
            traverse(child)
    
    traverse(main_func_node)
    
    print("\n=== 赋值操作收集结果 ===")
    for var, op, loop_label in assignments:
        print(f"操作: {var} {op} (循环标签: {loop_label})")
    return assignments