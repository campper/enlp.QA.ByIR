# coding:utf8
import os
import sys

work_directory = os.getcwd()

def aiml_question_parsing(question, T, mybot):
    input_message = question
    if len(input_message) > 60:
        print mybot.respond("句子长度过长")
    elif input_message.strip() == '':
        print mybot.respond("无")

    print input_message
    message = T.wordSegment(input_message)
    # 去标点
    # print 'word Seg:'+ message
    # print '词性：'
    words = T.postag(input_message)

    response = mybot.respond(message)

    return response

