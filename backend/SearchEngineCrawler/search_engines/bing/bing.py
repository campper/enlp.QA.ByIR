# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/4/16 下午3:26

from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine

class BingEngine(SearchEngine):
    """
    抓取Bing
    """
    def __init__(self,query='今天天气如何'):
        super(BingEngine,self).__init__()
        self.query = query
        self.url = 'https://www.baidu.com/s?wd=' + quote(self.query)
        self.html = ''
        self.flag = 0
        self.answer = []
        self.results = ''

    def __get_html(self):
        '''
        获取Bing网典的页面
        '''

        headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
        soup_bingwd = BeautifulSoup(requests.get(url=self.url,headers=headers,timeout = self.timeout).content, "lxml")

        # 去除无关的标签
        [s.extract() for s in soup_bingwd(['script', 'style', 'img', 'sup', 'b'])]
        # print(soup.prettify())
        return soup_bingwd

    def search(self):
        self.__get_html()
        self.flag = 0

        for i in range(1, self.num):
            if self.soup == None:
                break
            self.results = self.soup.find(id=i)
            if self.results == None:
                # logs.info("[{0}][func:{1}][line:{2}]:百度找不到答摘要摘要案".format(sys._getframe().f_code.co_filename,
                #                                                          sys._getframe().f_code.co_name,
                #                                                          sys._getframe().f_lineno))

                print("[{0}][func:{1}][line:{2}]:百度找不到答摘要摘要案".format(sys._getframe().f_code.co_filename,
                                                                     sys._getframe().f_code.co_name,
                                                                     sys._getframe().f_lineno))
                break
            else:
                yield self.results


