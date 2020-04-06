# coding:utf8

from AnswerGeneration.QACrawler.api import baike
from AnswerGeneration.QACrawler import search_summary
import requests
import sys
import time

def my_time():
    return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime())

def aiml_answer_generate(q_parsed, mybot, QAT, question):
    """
    add by songbc, 2018-01-28
    :param q_parsed: 问题经过解析后的形式，根据情况选择查询或者进行闲聊等等
    :param mybot: 传入一个mybot，对q_parsed的进行操作
    :param QAT: 处理网络查询返回的文件
    :param question: 原始问题，在特定条件下，直接用于搜索引擎搜索
    :return: ans，一个list，内部为答案，上层文件根据需要进行选择
    """
    response = q_parsed
    input_message = question

    try:

        if response == '':
            ans = [mybot.respond('找不到答案')]
        elif response[0] == '#':
            if response.__contains__("searchbaike"):
                print("search baike")
                print(response)
                res = response.split(':')
                #实体
                entity = str(res[1]).replace(" ","")
                #属性
                attr = str(res[2]).replace(" ","")
                print(entity+'<---->'+attr)

                ans = baike.query(entity, attr)
                # 如果命中答案
                if type(ans) == list:
                    ans = [QAT.ptranswer(ans, False)]
                elif ans.decode('utf-8').__contains__(u'::找不到'):
                    #百度摘要+Bing摘要
                    print("通用搜索")
                    ans = search_summary.kwquery(input_message)

            # 匹配不到模版，通用查询
            elif response.__contains__("NoMatchingTemplate"):
                print("NoMatchingTemplate")
                ans = search_summary.kwquery(input_message)


            if len(ans) == 0:
                ans = [mybot.respond('找不到答案')]
            else:
                ans = ans

            # 匹配模版
        else:
            # 这个分支似乎不会进入
            if type(response) == type([]):
                ans = response
            else:
                ans = [response]
    except requests.ConnectionError:
        ans = ['抱歉，我不知道如何回答您，等我再学习学习。'] # 未接入互联网 modified by zhangq 2018-03-28

    return ans

