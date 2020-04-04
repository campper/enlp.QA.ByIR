#coding:utf8
# 假定运行的目录是QA目录下
import aiml
import os
import sys
from pprint import pprint

sys.path.append(os.path.dirname(os.getcwd()))  # 增加模块寻址路径, 当前目录的上一层
pprint(sys.path)
print('@' * 40)


from Tools import Html_Tools as QAT
from Tools import TextProcess as T

from QuestionParser import aiml_parse
from AnswerGeneration import aiml_generate
import time

mybot = aiml.Kernel()
mybot.learn(os.path.split(os.path.realpath(__file__))[0]+"/resources/std-startup.xml")
mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bye.aiml")
mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")
mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bad.aiml")
mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/funny.aiml")
mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/OrdinaryQuestion.aiml")
mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/Common conversation.aiml")

T.jieba_initialize()


def qa(question, T, mybot, QAT):
    q_parsed = aiml_parse.aiml_question_parsing(question, T, mybot)
    ans = aiml_generate.aiml_answer_generate(q_parsed, mybot, QAT, question)
    return ans

def code_format(s):
    try:
        s = s.encode('utf8')
    except:
        s = s
    return s


if __name__ == "__main__":
    # question = raw_input('input something')
    # question = '的发烧发烧发烧地方'
    question = '姚明的爸爸是谁'
    # question = '你好'
    # ans = qa(question, T, mybot, QAT)
    # print '答案：', ans[0]
    # exit(0)

    old_out = sys.stdout
    # sys.stdout = open('/dev/null', 'w')  # 抛弃中间可能的print输出
    # flog = open('corpus-qa-log.txt', 'a')
    # qlog = open('corpus-qa-qlog.txt', 'a')
    #
    # print >> qlog, time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), os.getcwd()
    # print >> qlog, time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), os.path.abspath(os.curdir)
    # print >> qlog, time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), os.path.abspath('.')
    # print >> qlog, time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), 'sys.path add', sys.path.append(os.path.dirname(os.getcwd()))

    # question = sys.argv[1]
    # print >> qlog, time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), question
    # print >> qlog, '#' * 40
    # print >> qlog, time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), sys.argv[0]
    # print >> qlog, '#' * 40
    # question = "姚明是谁"
    # question = "分大赛佛鳄玩法"
    msg = qa(question, T, mybot, QAT)
    print msg
    print '$' * 30

    # 注意处理msg是列表还是字符串形式，对于列表，可能有多个答案。
    if type(msg) == type([]):
        if len(msg) == 1:
            msg = code_format(msg[0])
        else:
            # 编码情况放到最后统一进行
            opening = code_format("我得到了几个备选答案。\n")
            res = code_format('')
            for i in range(len(msg)):
                res += '%d) %s\n' % (i, code_format(msg[i].encode('utf8')))
            msg = opening + res

    else:
        pass

    sys.exit(0)
