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

# ===== 提取 for 循环（带 label） =====
def extract_loops(node, source_code):
    loops = []
    global undefined_loop_n
    
    def traverse(n, parent_loop=None, current_label_path=[]):
        if n.type == 'for_statement':
            parent = n.parent
            label = None
            if parent and parent.type == 'labeled_statement':
                label_node = parent.children[0]
                label = source_code[label_node.start_byte:label_node.end_byte]
            else:
                global undefined_loop_n
                undefined_loop_n += 1
                label = f"loop_{undefined_loop_n}"  # 更明确的默认标签
            
            new_label_path = current_label_path.copy()
            new_label_path.append(label)
            
            loop_info = {
                'label': label,
                'start_byte': n.start_byte,
                'end_byte': n.end_byte,
                'label_path': new_label_path,
                'inner_loops': []
            }
            
            if parent_loop:
                parent_loop['inner_loops'].append(loop_info)
            else:
                loops.append(loop_info)
            
            for child in n.children:
                traverse(child, loop_info, new_label_path)
        else:
            for child in n.children:
                traverse(child, parent_loop, current_label_path)
    
    traverse(node)
    return loops
