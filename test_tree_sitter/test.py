# -*- coding: utf-8 -*-
from tree_sitter import Language, Parser
import tree_sitter_c

# 创建解析器
parser = Parser()

# 获取 C 语言
C_LANGUAGE = Language(tree_sitter_c.language())
parser.language = C_LANGUAGE

# 测试代码
c_code = """
int main() {
    printf("Hello, Tree-sitter!");
    return 0;
}
"""

try:
    # 解析代码
    tree = parser.parse(bytes(c_code, 'utf8'))
    
    # 获取根节点并打印
    print("解析结果：")
    
    # 打印更详细的信息
    def print_tree(node, level=0):
        indent = "  " * level
        print(f"{indent}- {node.type}: {node.text.decode('utf8')}")
        for child in node.children:
            print_tree(child, level + 1)
    
    print_tree(tree.root_node)
    
except Exception as e:
    print(f"发生错误：{str(e)}")