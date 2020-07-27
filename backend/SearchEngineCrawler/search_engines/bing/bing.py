# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/4/16 下午3:26

import sys
from urllib.parse import quote
import urllib
import urllib3
import re
from bs4 import BeautifulSoup
import requests,time

from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine

class BingEngine(SearchEngine):
    """
    抓取Bing
    """
    def __init__(self,query='今天天气如何'):
        super(BingEngine,self).__init__()
        self.query = query
        self.url = 'https://cn.bing.com/search?q=' + quote(self.query)
        self.html = ''
        self.flag = 0
        self.answer = []
        self.setting_pages(10)
        self.results = []

    def setting_pages(self,num):
        """
        # 检索条目设置
        """
        self.num = num

    def __get_html(self):
        '''
        获取Bing网典的页面
        '''

        headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
        try:
            soup_bingwd = BeautifulSoup(requests.get(url=self.url,headers=headers,timeout = self.timeout).content, "lxml")

            # 去除无关的标签
            [s.extract() for s in soup_bingwd(['script', 'style', 'img', 'sup', 'b'])]
            # print(soup.prettify())
            self.soup = soup_bingwd
        except Exception as err:
            raise err

    def search(self):
        self.__get_html()
        self.flag = 0

        if self.soup != None:
            for i in range(1, self.num):
                result = self.soup.find(id=i)
                if result == None:
                    # logs.info("[{0}][func:{1}][line:{2}]:百度找不到答摘要摘要案".format(sys._getframe().f_code.co_filename,
                    #                                                          sys._getframe().f_code.co_name,
                    #                                                          sys._getframe().f_lineno))

                    print("[{0}][func:{1}][line:{2}]:微软bing找不到答摘要摘要案".format(sys._getframe().f_code.co_filename,
                                                                         sys._getframe().f_code.co_name,
                                                                         sys._getframe().f_lineno))
                    break
                else:
                    yield result
                self.results.append(result)
            else:
                print("未抓取到")


