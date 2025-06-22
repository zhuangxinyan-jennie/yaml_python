import re
import os
import argparse

# 默认初始化值（根据类型）
default_init = {
    'int': '0', 'float': '0.0f', 'double': '0.0', 'char': "'\\0'", 'long': '0L',
    'short': '0', 'unsigned': '0', 'bool': 'false', 'signed': '0',
    'int8_t': '0', 'int16_t': '0', 'int32_t': '0', 'int64_t': '0',
    'uint8_t': '0', 'uint16_t': '0', 'uint32_t': '0', 'uint64_t': '0',
    'size_t': '0'
}

# 正则定义
macro_pattern = re.compile(r'#define\s+(\w+)\s+([\w\d_]+)')
include_pattern = re.compile(r'#include\s+"([^"]+)"')

type_keywords = [
    r'int', r'float', r'double', r'char', r'long', r'short',
    r'unsigned', r'bool', r'signed', r'int\d+_t', r'uint\d+_t', r'size_t'
]
type_pattern = r'(?:' + r'|'.join(type_keywords) + r'|\w+)'
decl_pattern = re.compile(
    rf'^\s*({type_pattern}(?:\s+{type_pattern})*)\s+([a-zA-Z_]\w*(?:\s*,\s*[a-zA-Z_]\w*)*)\s*;',
    re.MULTILINE
)

# 提取宏定义
def extract_macros(code):
    return dict(macro_pattern.findall(code))

# 提取本地 include
def extract_includes(code):
    return include_pattern.findall(code)

# 替换类型宏
def resolve_type(decl_type, macro_map):
    words = decl_type.split()
    resolved = []
    for word in words:
        while word in macro_map:
            word = macro_map[word]
        resolved.append(word)
    return ' '.join(resolved)

# 获取默认值
def get_default_value(decl_type):
    for key in default_init:
        if key in decl_type.split():
            return default_init[key]
    return '0'

# 替换声明为初始化声明
def transform_declaration(decl_type, variables, macro_map, expand_macros=False):
    resolved_type = resolve_type(decl_type, macro_map)
    default_val = get_default_value(resolved_type)
    var_list = [v.strip() for v in variables.split(',')]
    initialized = [f"{v} = {default_val}" for v in var_list]
    if expand_macros:
        return f"{resolved_type} {', '.join(initialized)};"
    else:
        return f"{decl_type} {', '.join(initialized)};"

# 解析 include 文件中的宏
def load_included_macros(source_path, code):
    root_dir = os.path.dirname(source_path)
    all_macros = {}

    included_files = extract_includes(code)
    for inc in included_files:
        inc_path = os.path.normpath(os.path.join(root_dir, inc))
        if os.path.exists(inc_path):
            with open(inc_path, "r", encoding="utf-8") as f:
                inc_code = f.read()
            macros = extract_macros(inc_code)
            all_macros.update(macros)

    return all_macros

# 替换所有未初始化的变量
def initialize_variables(code, macro_map, expand_macros=False):
    def replacer(match):
        decl_type, variables = match.groups()
        if '=' in variables:
            return match.group(0)
        return transform_declaration(decl_type, variables, macro_map, expand_macros)
    return decl_pattern.sub(replacer, code)

# 主处理函数
def process_file(file_path, expand_macros=False):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    macro_map = extract_macros(code)
    macro_map.update(load_included_macros(file_path, code))

    return initialize_variables(code, macro_map, expand_macros)

# 命令行接口
def main():
    parser = argparse.ArgumentParser(description="初始化未赋值的变量声明")
    parser.add_argument("source", help="输入 C 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--expand-macros", action="store_true", help="是否展开类型宏（如 TYPE -> double）")

    args = parser.parse_args()

    result = process_file(args.source, expand_macros=args.expand_macros)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"已写入至 {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()

'''
# 默认：仅补全未初始化的变量
python Add_Predefine.py example.c

# 输出至文件
python Add_Predefine.py example.c -o out.c

# 同时展开宏（如 TYPE -> double）
python Add_Predefine.py example.c -o out.c --expand-macros

'''