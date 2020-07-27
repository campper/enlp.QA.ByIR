# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/7/27 下午1:22
from backend.SearchEngineCrawler.search_engines.bing.bing import BingEngine

def test():
    query ='国家电网公司'
    bing = BingEngine(query)

    for no,result in enumerate(bing.search()):
        text = result.text.replace(' ','').replace('\n','').replace('\r','')
        print("[{}]:{}".format(no+1,text))
        stop = 1
    print(len(bing.results))

if __name__ == '__main__':
    test()