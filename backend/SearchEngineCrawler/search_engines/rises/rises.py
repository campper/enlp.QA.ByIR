# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/5/2 下午1:22

from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine

class RisesEngine(SearchEngine):
    """
    抓取能源语义搜索引擎结果
    """

    def __init__(self):
        super(RisesEngine,self).__init__()
        self.query = super().query
        self.url = 'https://rises.tech/result?_kw={}&tab=news'.format(quote(self.query)) # result?_kw=资讯&tab=news
        self.html = ''
        self.flag = 0
        self.answer = []
        self.results = ''