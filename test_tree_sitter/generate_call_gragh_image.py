#utf-8
#---utf-8---
from tree_sitter import Language,Parser
import tree_sitter_c
from graphviz import Digraph # type: ignore

try:
    C_LANGUAGE = Language(tree_sitter_c.language())
    parser = Parser()
    parser.language = C_LANGUAGE
except Exception as e:
    C_LANGUAGE = Language('build/c-lang.so', 'c')
    parser = Parser()
    parser.set_language(C_LANGUAGE)




def generate_call_graph_image(call_map, output_file='call_graph'):
    dot = Digraph(comment='Function Call Graph')
    for caller, callees in call_map.items():
        dot.node(caller)
        for callee in callees:
            dot.node(callee)
            dot.edge(caller, callee)
    dot.render(output_file, format='png', cleanup=True)
    print(f"[?] 函数调用图已生成：{output_file}.png")