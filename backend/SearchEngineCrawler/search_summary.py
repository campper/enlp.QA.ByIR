#coding:utf8
import sys
import time
from urllib.parse import quote

from common_tools import Html_Tools as To
from utils import TextProcess as T
import logs

def kwquery(query):
    # 分词 去停用词 抽取关键词，抽取实体
    words = T.postag(query)
    # 获取对应模式下的词语
    keywords = T.entity_extract_by_postag(words,"n")

    answer = []
    text = ''

    # 找到答案就置
    flag = 0

    # 抓取百度前10条的摘要


    #获取bing的摘要
    soup_bing = To.get_html_bing('https://www.bing.com/search?q='+quote(query))
    # 判断是否在Bing的知识图谱中
    # bingbaike = soup_bing.find(class_="b_xlText b_emphText")
    bingbaike = soup_bing.find(class_="bm_box")

    if bingbaike != None:
        if bingbaike.find_all(class_="b_vList")[1] != None:
            if bingbaike.find_all(class_="b_vList")[1].find("li") != None:
                print("Bing知识图谱找到答案")
                flag = 1
                answer.append(bingbaike.get_text())
                # print "====="
                # print answer
                # print "====="
                return answer
    else:
        print("Bing知识图谱找不到答案")
        results = soup_bing.find(id="b_results")
        bing_list = results.find_all('li')
        for bl in bing_list:
            temp = bl.get_text()
            if temp.__contains__(u" - 必应网典"):
                print("查找Bing网典")
                url = bl.find("h2").find("a")['href']
                if url is None:
                    print("Bing网典找不到答案")
                    continue
                else:
                    print("Bing网典找到答案")
                    bingwd_soup = To.get_html_bingwd(url)

                    r = bingwd_soup.find(class_='bk_card_desc').find("p")
                    if r is None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break
            if temp.__contains__(u"百度百科"):
                print('从bing进入百度百科')
                url = bl.find("h2").find("a")['href']
                if url == None:
                    print("百度百科找不到答案")
                    continue
                else:
                    print("百度百科找到答案")
                    baike_soup = To.get_html_baike(url)

                    r = baike_soup.find(class_='lemma-summary')
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n","").strip()
                    answer.append(r)
                    flag = 1
                    break

        if flag == 1:
            return answer

        text += results.get_text()

    # print text


    # 如果再两家搜索引擎的知识图谱中都没找到答案，那么就分析摘要
    if flag == 0:
        #分句
        cutlist = [u"。",u"?",u".", u"_", u"-",u":",u"！",u"？"]
        temp = ''
        sentences = []
        for i in range(0,len(text)):
            if text[i] in cutlist:
                if temp == '':
                    continue
                else:
                    # print temp
                    sentences.append(temp)
                temp = ''
            else:
                temp += text[i]

        # 找到含有关键词的句子,去除无关的句子
        key_sentences = {}
        for s in sentences:
            for k in keywords:
                if k in s:
                    key_sentences[s]=1


        # 根据问题制定规则

        # 识别人名?为什么要识别人名
        target_list = {}
        for ks in key_sentences:
            # print ks
            words = T.postag(ks)
            for w in words:
                # print "====="
                # print w.word
                if w.flag == ("nr"):
                    # if target_list.has_key(w.word):
                    if w.word in target_list:
                        target_list[w.word] += 1
                    else:
                        target_list[w.word] = 1

        # 找出最大词频
        # sorted_lists = sorted(target_list.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        sorted_lists = sorted(target_list.items(),key=lambda x:x[1],reverse=True)
        # print len(target_list)
        #去除问句中的关键词
        sorted_lists2 = []
        # 候选队列
        for i, st in enumerate(sorted_lists):
            # print st[0]
            if st[0] in keywords:
                continue
            else:
                sorted_lists2.append(st)

        print("返回前n个词频")
        answer = []
        for i,st in enumerate(sorted_lists2):
            # print st[0]
            # print st[1]
            if i< 3:
                # print st[0]
                # print st[1]
                answer.append(st[0])
        # print answer

    return answer


if __name__ == '__main__':
    pass
    query = "中国四大美女"
    ans = kwquery(query)
    print("~~~~~~~")
    for a in ans:
        print(a)
    print("~~~~~~~")
