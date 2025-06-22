# -*- coding: utf-8 -*-
from tree_sitter import Language, Parser
import tree_sitter_c
from graphviz import Digraph

# ��ʼ�� Tree-sitter
try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)

def create_ast_graph(root_node, max_depth=5):
    dot = Digraph(comment='Abstract Syntax Tree')
    dot.attr(rankdir='TB')
    
    # ��������Ψһ�Ľڵ�ID
    node_count = [0]
    
    def add_node(node, depth=0):
        if depth > max_depth:
            return
        
        # ����Ψһ�Ľڵ�ID
        node_id = str(node_count[0])
        node_count[0] += 1
        
        # ��ȡ�ڵ��ı�������Ǳ�ʶ������������
        node_text = ""
        if len(node.children) == 0:
            try:
                node_text = node.text.decode('utf-8')
                if node_text.strip():
                    node_text = f"\n'{node_text}'"
            except:
                pass
        
        # ���ӽڵ�
        label = f"{node.type}{node_text}"
        dot.node(node_id, label)
        
        # �ݹ鴦���ӽڵ�
        for child in node.children:
            child_id = str(node_count[0])
            add_node(child, depth + 1)
            dot.edge(node_id, child_id)
    
    # �Ӹ��ڵ㿪ʼ����ͼ
    add_node(root_node)
    return dot

# ��ȡC�ļ�
with open('aes.c', 'r', encoding='utf-8') as f:
    code = f.read()

# ��������
tree = parser.parse(bytes(code, 'utf8'))
root_node = tree.root_node

# ����ASTͼ
ast_graph = create_ast_graph(root_node)

# ����ͼƬ
ast_graph.render('aes_ast', format='png', cleanup=True)
print("ASTͼ�ѱ���Ϊ aes_ast.png") 