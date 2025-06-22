import argparse
import tempfile
import os

# 导入各个模块的 main 函数
from Add_Predefine import main as add_predefine_main
from Del_Annotation import main as del_annotation_main
from Generator_treeSitter import main as generator_main

def main():
    parser = argparse.ArgumentParser(description="预处理并分析 C 代码，输出 YAML 配置和调用图")
    
    parser.add_argument("source", help="原始 C 源码路径")
    parser.add_argument("--expand-macros", action="store_true", help="是否展开类型宏（如 TYPE -> double）")
    parser.add_argument("--draw-callgraph", action="store_true", help="是否绘制调用图")
    parser.add_argument("-o", "--output", help="YAML 输出路径（可选）")

    args = parser.parse_args()

    # 临时文件路径
    with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmp1:
        tmp1_path = tmp1.name
    with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmp2:
        tmp2_path = tmp2.name

    # 构造 Add_Predefine 参数
    import sys
    sys.argv = ['Add_Predefine.py', args.source, '-o', tmp1_path]
    if args.expand_macros:
        sys.argv.append('--expand-macros')
    print(f"[*] Running Add_Predefine...")
    add_predefine_main()

    # 构造 Del_Annotation 参数
    sys.argv = ['Del_Annotation.py', tmp1_path, tmp2_path]
    print(f"[*] Running Del_Annotation...")
    del_annotation_main()

    # 构造 Generator_treeSitter 参数
    sys.argv = ['Generator_treeSitter.py', tmp2_path]
    if args.draw_callgraph:
        sys.argv.append('--draw-callgraph')
    if args.output:
        sys.argv.extend(['--output', args.output])
    print(f"[*] Running Generator_treeSitter...")
    generator_main()

    # 清理临时文件
    os.remove(tmp1_path)
    os.remove(tmp2_path)
    print("[✓] 所有处理完成")

if __name__ == "__main__":
    main()


'''
python launch.py input.c --expand-macros --draw-callgraph -o result.yaml

1.用 Add_Predefine.py 预处理 input.c 并展开宏（如果指定）；
2.接着用 Del_Annotation.py 删除注释；
3.最后用 Generator_treeSitter.py 生成 .yaml 和调用图（如果指定）；

支持用户自定义 .yaml 输出路径。
'''