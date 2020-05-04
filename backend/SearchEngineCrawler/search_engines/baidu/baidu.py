import sys
from urllib.parse import quote
import urllib
import re
from bs4 import BeautifulSoup
import requests,time

from backend.SearchEngineCrawler.common_tools import html_tools as To
from backend.utils import TextProcess as T

from backend.SearchEngineCrawler.search_engines.base.BaseEngine import SearchEngine
import backend.logs

class BaiduEngine(SearchEngine):

    def __init__(self,query='今天天气如何'):
        """
        初始化检索引擎
        """
        super(BaiduEngine,self).__init__()
        self.query = query
        self.url = 'https://www.baidu.com/s?wd=' + quote(self.query)
        self.html = ''
        self.setting_pages(10)
        self.flag = 0
        self.answer = []
        self.results = ''

    def setting_pages(self,num):
        """
        # 检索条目设置
        """
        self.num = num

    '''
    获取百度搜索的结果
    '''
    def __get_html(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
        try:
            soup_baidu = BeautifulSoup(requests.get(url=self.url, headers=headers).content.decode('utf-8'), "lxml")
            # 去除无关的标签
            [s.extract() for s in soup_baidu(['script', 'style', 'img'])]
            self.soup = soup_baidu
        except Exception as err:
            raise err

    def search_from_zhidao(self):
        # 判断是否有mu,如果第一个是百度知识图谱的 就直接命中答案
        # if results.attrs.has_key('mu') and i== 1:
        if 'mu' in self.results.attrs and i == 1:
            # print results.attrs["mu"]
            r = self.results.find(class_='op_exactqa_s_answer')
            if r == None:
                print("[{0}][func:{1}][line:{2}]:百度知识图谱找不到答案".format(sys._getframe().f_code.co_filename,
                                                                     sys._getframe().f_code.co_name,
                                                                     sys._getframe().f_lineno))
            else:
                # print r.get_text()
                print("[{0}][func:{1}][line:{2}]:百度知识图谱找到答案".format(sys._getframe().f_code.co_filename,
                                                                    sys._getframe().f_code.co_name,
                                                                    sys._getframe().f_lineno))
                self.answer.append(r.get_text().strip())
                self.flag = 1

    def get_poetry(self):
        # 古诗词判断
        # if results.attrs.has_key('mu') and i == 1:
        if 'mu' in self.results.attrs and i == 1:
            r = self.results.find(class_="op_exactqa_detail_s_answer")
            if r == None:
                print("[{0}][func:{1}][line:{2}]:百度诗词找不到答案".format(sys._getframe().f_code.co_filename,
                                                                   sys._getframe().f_code.co_name,
                                                                   sys._getframe().f_lineno))
                print("百度诗词找不到答案")
            else:
                # print r.get_text()
                # print("百度诗词找到答案")
                print("[{0}][func:{1}][line:{2}]:百度诗词找到答案".format(sys._getframe().f_code.co_filename,
                                                                  sys._getframe().f_code.co_name,
                                                                  sys._getframe().f_lineno))
                self.answer.append(r.get_text().strip())
                self.flag = 1

    def get_perpetual_calendar(self):
        # 万年历 & 日期
        if 'mu' in self.results.attrs and i == 1 and self.results.attrs['mu'].__contains__('http://open.baidu.com/calendar'):
            r = results.find(class_="op-calendar-content")
            if r == None:
                print("百度万年历找不到答案")
            else:
                # print r.get_text()
                print("百度万年历找到答案")
                self.answer.append(r.get_text().strip().replace("\n", "").replace(" ", ""))
                self.flag = 1

        if 'tpl' in self.results.attrs and i == 1 and self.results.attrs['tpl'].__contains__('calendar_new'):
            r = self.results.attrs['fk'].replace("6018_", "")
            print(r)

            if r == None:
                print("百度万年历新版找不到答案")
                # continue
            else:
                # print r.get_text()
                print("百度万年历新版找到答案")
                self.answer.append(r)
                self.flag = 1

    def get_calcuator(self):
        # 计算器
        if 'mu' in self.results.attrs and i == 1 and self.results.attrs['mu'].__contains__(
                'http://open.baidu.com/static/calculator/calculator.html'):
            r = self.results.find('div').find_all('td')[1].find_all('div')[1]
            if r == None:
                print("计算器找不到答案")
                # continue
            else:
                # print r.get_text()
                print("计算器找到答案")
                self.answer.append(r.get_text().strip())
                self.flag = 1

    def get_zhidao(self):
        if 'mu' in self.results.attrs and i == 1:
            r = self.results.find(class_='op_best_answer_question_link')
            if r == None:
                # print("百度知道图谱找不到答案")
                print("[{0}][func:{1}][line:{2}]:百度知道图谱找不到答案".format(sys._getframe().f_code.co_filename,
                                                                     sys._getframe().f_code.co_name,
                                                                     sys._getframe().f_lineno))
            else:
                # print("百度知道图谱找到答案")
                print("[{0}][func:{1}][line:{2}]:百度知道图谱找到答案".format(sys._getframe().f_code.co_filename,
                                                                    sys._getframe().f_code.co_name,
                                                                    sys._getframe().f_lineno))
                url = r['href']
                zhidao_soup = To.get_html_zhidao(url)
                r = zhidao_soup.find(class_='bd answer').find('pre')
                if r == None:
                    r = zhidao_soup.find(class_='bd answer').find(class_='line content')

                self.answer.append(r.get_text())
                self.flag = 1

        if self.results.find("h3") != None:
            # 百度知道
            if self.results.find("h3").find("a").get_text().__contains__(u"百度知道") and (i == 1 or i == 2):
                url = self.results.find("h3").find("a")['href']
                if url == None:
                    print("百度知道图谱找不到答案")
                else:
                    print("百度知道图谱找到答案")
                    zhidao_soup = To.get_html_zhidao(url)

                    r = zhidao_soup.find(class_='bd answer')
                    if r == None:
                        pass
                    else:
                        r = r.find('pre')
                        if r == None:
                            r = zhidao_soup.find(class_='bd answer').find(class_='line content')
                    self.answer.append(r.get_text().strip())
                    self.flag = 1

    def get_baike(self):
        # 百度百科
        if self.results.find("h3").find("a").get_text().__contains__(u"百度百科") and (i == 1 or i == 2):
            url = self.results.find("h3").find("a")['href']
            if url == None:
                print("百度百科找不到答案")
                pass
            else:
                print("百度百科找到答案")
                baike_soup = To.get_html_baike(url)

                r = baike_soup.find(class_='lemma-summary')
                if r == None:
                    pass
                else:
                    r = r.get_text().replace("\n", "").strip()
                self.answer.append(r)
                self.flag = 1

    def process(self):
        """
        抓取百度结果策略
        """
        text += self.results.get_text()

        if self.flag == 1:
            return self.answer

    def kwquery(self):
        """
        检索主函数
        """
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

def test():
    query ='国家电网公司'
    baidu = BaiduEngine(query)
    for result in baidu.kwquery():
        print(result)
        stop = 1

if __name__ == '__main__':
    test()