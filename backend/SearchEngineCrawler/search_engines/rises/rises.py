# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/5/2 下午1:22
import json


from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine

class RisesEngine(SearchEngine):
    """
    抓取能源语义搜索引擎结果
    api:https://rises.tech/api/search?_kw=%E9%98%B6%E6%A2%AF%E7%94%B5%E4%BB%B7&_page=1&_size=10
    """

    def __init__(self):
        super(RisesEngine,self).__init__()
        self.page = 0
        self.size = 10
        self.query = super().query
        self.url = 'https://rises.tech/api/search?_kw={0}&_page={1}&_size={2}'.format(quote(self.query),self.page,self.size) # result?_kw=资讯&tab=news
        self.html = ''
        self.flag = 0
        self.answer = []
        self.results = ''
