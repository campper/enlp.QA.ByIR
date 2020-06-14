# -*- coding:utf-8 -*-
# Author:   icowin
# Project:  nlp.QA.ByIR   
# Date: 2020/5/15 下午4:02
import os
import time
import Getbrowser
import unittest

class RunSogou(unittest.TestCase): #新建一个unittest的TestCase的类
   def setUp(self):  #运行测试用例前需要执行的方法
        self.driver = Getbrowser.Chrome()

   def testRunSogou(self):
       # 测试用例主方法,必须以test开头命名,否则无法运行
       driver = self.driver
       driver.get("http://www.sogou.com")
       time.sleep(2)
       self.assertIn('搜狗搜索', driver.title)
       time.sleep(2)


if __name__ == '__main__':
    unittest.main()