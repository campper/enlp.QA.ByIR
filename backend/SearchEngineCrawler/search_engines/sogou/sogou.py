# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/5/13 下午2:18


from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine

class SogouEngine(SearchEngine):
    """
    抓取能源语义搜索引擎结果
    api:https://rises.tech/api/search?_kw={$query}&_page=1&_size=10
    """

    def __init__(self):
        super(SogouEngine,self).__init__()
        self.page = 0
        self.size = 10
        self.query = super().query
        self.url = 'https://www.sogou.com/web?query={0}&_page={1}&_size={2}'.format(quote(self.query),self.page,self.size) # result?_kw=资讯&tab=news
        self.html = ''
        self.flag = 0
        self.answer = []
        self.results = ''