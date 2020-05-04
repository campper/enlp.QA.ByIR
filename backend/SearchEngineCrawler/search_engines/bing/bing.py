# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/4/16 下午3:26

from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine

class BingEngine(SearchEngine):
    """
    抓取Bing
    """
    def __init__(self):
        super(BingEngine,self).__init__()
        self.query = query
        self.url = 'https://www.baidu.com/s?wd=' + quote(self.query)
        self.html = ''
        self.flag = 0
        self.answer = []
        self.results = ''

