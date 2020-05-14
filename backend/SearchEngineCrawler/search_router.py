# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/5/13 下午2:06

import sys
import time
from urllib.parse import quote

from backend.SearchEngineCrawler.common_tools import html_tools as To
from backend.SearchEngineCrawler.search_engines.baidu import baidu,baike
from backend.SearchEngineCrawler.search_engines.bing import bing
from backend.SearchEngineCrawler.search_engines.rises import rises
from backend.SearchEngineCrawler.search_engines.sogou import sogou
from backend.utils import TextProcess as T
import backend.logs

def kwquery(query):
    # 分词 去停用词 抽取关键词，抽取实体
    words = T.postag(query)
    # 获取对应模式下的词语
    keywords = T.entity_extract_by_postag(words, "n")

    # 将检索词在几个搜索引擎里找答案
    # baidu
    baidu_search = baidu.BaiduEngine(query)
    results = baidu_search.search()

    # bing
    bing_search = bing.BingEngine(query)
    results = bing_search.search()

if __name__ == '__main__':
    query= "国家电网公司"
    kwquery(query)