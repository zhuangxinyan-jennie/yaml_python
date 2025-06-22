import argparse
from tree_sitter import Language, Parser
import yaml # type: ignore
import os
from graphviz import Digraph # type: ignore

import tree_sitter_c
from interList import interList
from funcList import funcList
from find_top_func import find_top_func
from find_arrList import find_arrList
from get_parser import get_parser
from generate_call_gragh_image import generate_call_graph_image
from parse_header_macros import parse_header_macros
from extract_loops import extract_loops
from extract_function_calls import extract_function_calls
from generate_dict_op import generate_dict_op
from collect_assignments import collect_assignments
from collect_variable_declarations import collect_variable_declarations
from detect_top_function_via_call_gragh import detect_top_function_via_call_graph

# ===== 构造配置文件 =====
def generate_config_yaml(top_func, func_calls, loops, variables,assignments,tree,source_code):
    # 0410 改动 写interList的结果形式
    param_list = interList(source_code)
    func_calls = funcList(source_code)
    top_func = find_top_func(source_code)
    arr_list = find_arrList(source_code)
    
    if isinstance(top_func, list):
        top_func = top_func[0]

    config = {
        'top': [top_func],
        'funcList': func_calls,
        'loopList': {},
        'dictOp': {
            'int': {},
            'float': [],
            'double': [],
            'half': []
        },
        # 'interList': [f"{top_func} k", f"{top_func} buf"],
        'interList':[
             f"{top_func} {i}" for i in param_list
        ],
        'arrList': [
            f"{top_func} {i}" for i in arr_list
        ]
    }

        # === 原 loopList 构建逻辑 ===
    def collect_loop_groups(loop, group_name):
        label_list = []
        def collect_labels(loop_node):
            full_label = f"{top_func}/{loop_node['label']}"
            label_list.append(full_label)
            for child in loop_node.get('inner_loops', []):
                collect_labels(child)
        collect_labels(loop)
        config['loopList'][group_name] = {
            'level': label_list,
            'unroll': label_list,
            'pipeline': [label_list[-1]],
            'flatten': []
        }

    for idx, loop in enumerate(loops, 1):
        group_name = f"group{idx}"
        collect_loop_groups(loop, group_name)

    dict_op = generate_dict_op(top_func, variables, assignments)
    config['dictOp'] = dict_op

    return config

# ===== 主处理逻辑 =====
def process_file(c_file, draw_graph=False):
    filename = os.path.basename(c_file)
    file_prefix = os.path.splitext(filename)[0]  # 获取无扩展名的文件名作为函数前缀

    with open(c_file, 'r', encoding='utf-8') as f:
        source_code = f.read()

    # 新增：解析所有关联头文件中的宏定义
    macro_map = parse_header_macros(c_file, source_code)
    print(f"[DEBUG] 宏定义映射表: {macro_map}")

    parser = get_parser()
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    top_func, call_map = detect_top_function_via_call_graph(root_node, source_code)
    if not top_func:
        top_func = file_prefix + '_main'

    if draw_graph:
        generate_call_graph_image(call_map, output_file='call_graph')

    main_func_node = None
    def find_main_function(node):
        nonlocal main_func_node
        if node.type == 'function_definition':
            declarator = node.child_by_field_name('declarator')
            identifier = None
            if declarator:
                for child in declarator.children:
                    if child.type == 'identifier':
                        identifier = source_code[child.start_byte:child.end_byte]
                        break
            if identifier == top_func:
                main_func_node = node
        for child in node.children:
            find_main_function(child)
    find_main_function(root_node)

    if main_func_node:
        loops = extract_loops(main_func_node, source_code)
    else:
        loops = []

    func_calls = extract_function_calls(root_node, source_code, file_prefix)
    variables = collect_variable_declarations(main_func_node, source_code, macro_map)
    assignments = collect_assignments(main_func_node, source_code, loops)

    return generate_config_yaml(top_func, func_calls, loops, variables, assignments, tree, source_code)

# ===== CLI 主入口 =====
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('c_file', help='Input C file path')
    parser.add_argument('--draw-callgraph', action='store_true', help='Generate call graph image')
    parser.add_argument('--output', '-o', help='YAML output file path (optional)')
    args = parser.parse_args()

    config = process_file(args.c_file, draw_graph=args.draw_callgraph)


    # 0410 改动 写格式
    yaml_str = yaml.dump(config, default_flow_style=False, sort_keys=False, indent=4)
    lines = yaml_str.split('\n')
    new_lines = []
    current_key = None
    
    for line in lines:
        stripped = line.strip()
        if stripped.endswith(':'):  # 找到键
            current_key = stripped[:-1]  # 去掉冒号
            new_lines.append(line)
        elif stripped.startswith('- '):  # 处理列表项
            if current_key in ['top', 'funcList', 'level', 'unroll', 'pipeline', 'flatten', 'float', 'double', 'half', 'arrList', 'interList']:
                # 给这些键下的列表项添加额外的缩进
                new_lines.append('    ' + line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            if ':' in line:
                current_key = line.split(':')[0].strip()
    
    yaml_str = '\n'.join(new_lines)
    

    print("# === 生成的配置文件 (YAML 格式) ===")
    print(yaml_str)

    # 写入 YAML 文件
    if args.output:
        out_path = args.output
    else:
        out_path = os.path.splitext(args.c_file)[0] + '.yaml'

    with open(out_path, 'w') as f:
        f.write(yaml_str)
        print(f"YAML 配置文件已保存到: {out_path}")

if __name__ == '__main__':
    main()
