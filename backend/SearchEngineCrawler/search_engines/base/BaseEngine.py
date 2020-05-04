# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/4/17 下午4:22
import sys
sys.path.append(".")

class SearchEngine():
    """
    搜索引擎基类
    """
    def __init__(self):
        self.query = ''
        self.url = ''
        self.html = ''
