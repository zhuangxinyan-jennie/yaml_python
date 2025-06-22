# -*- coding: utf-8 -*-
from tree_sitter import Language

# 构建 Python 语言库
Language.build_library(
    # 存储生成的.so文件的路径
    'my-languages.so',
    
    # 包含语法的仓库路径
    [
        'tree-sitter-python'  # 这里假设你已经安装了 tree-sitter-python
    ]
) 