# -*- coding: utf-8 -*-
from tree_sitter import Language

# ���� Python ���Կ�
Language.build_library(
    # �洢���ɵ�.so�ļ���·��
    'my-languages.so',
    
    # �����﷨�Ĳֿ�·��
    [
        'tree-sitter-python'  # ����������Ѿ���װ�� tree-sitter-python
    ]
) 