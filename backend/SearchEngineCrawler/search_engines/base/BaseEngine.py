# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/4/17 下午4:22
import sys
sys.path.append(".")

class SearchEngine():
    """
    搜索引擎抓取基类
    """
    def __init__(self):
        self.query = ''
        self.url = ''
        self.html = ''
        self.timeout = 10
        self.charset = 'utf-8'

