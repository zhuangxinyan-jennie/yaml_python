#---utf-8---
from tree_sitter import Language,Parser
import tree_sitter_c
import re
import os

try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)

def parse_header_macros(c_file_path, source_code):
    """解析所有关联头文件中的宏定义（支持多层嵌套）"""
    macro_map = {}
    
    # 匹配 #include 语句
    include_pattern = re.compile(r'#include\s+["<](.+?)[">]')
    #=============================================================0411#
    # define_pattern = re.compile(r'#define\s+(\w+)(?:\(.*?\))?\s+(.+)$', re.MULTILINE)
    define_pattern = re.compile(r'#define\s+(\w+)(?:\([^)]*\))?\s+(.*?)(?=\n#|$)', re.MULTILINE | re.DOTALL)
    
    for macro, value in define_pattern.findall(source_code):
        macro_map[macro] = value
        print(f"macro: {macro}, value: {value}")




    # 递归解析头文件
    def parse_file(file_path, visited):
        if file_path in visited:
            return
        visited.add(file_path)
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # 提取宏定义（简单场景：处理 #define MACRO value 形式）
                # define_pattern = re.compile(r'#define\s+(\w+)\s+([^\s]+)')
                define_pattern = re.compile(r'#define\s+(\w+)(?:\(.*?\))?\s+(.+)$', re.MULTILINE)
                for macro, value in define_pattern.findall(content):
                    macro_map[macro] = value
                
                # 递归处理嵌套的 #include
                for match in include_pattern.findall(content):
                    header_path = os.path.join(os.path.dirname(file_path), match)
                    if os.path.exists(header_path):
                        parse_file(header_path, visited)
        except FileNotFoundError:
            pass
    
    # 初始解析当前 C 文件所在目录的头文件
    base_dir = os.path.dirname(c_file_path)
    initial_headers = include_pattern.findall(source_code)
    visited = set()
    for header in initial_headers:
        header_path = os.path.join(base_dir, header)
        if os.path.exists(header_path):
            parse_file(header_path, visited)
    
    # 解析宏的链式定义（如 #define TYPE REAL，再 #define REAL double）
    # for macro in list(macro_map.keys()):
    #     current_value = macro_map[macro]
    #     while current_value in macro_map:
    #         current_value = macro_map[current_value]
    #     macro_map[macro] = current_value
    
    return macro_map