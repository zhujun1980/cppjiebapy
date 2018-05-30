# encoding: utf-8

"""
 * C++JieBa Python Binding
 *
 * @author zhujun
 * @weibo @半饱半醉
 * @time 2018-05-30
"""

import sys
sys.path.append("../python")
from cppjiebapy import load_lib

DLL = load_lib("../build")
jieba = DLL.create_jieba("../dict/jieba.dict.utf8",
                         "../dict/hmm_model.utf8",
                         "../dict/user.dict.utf8",
                         "../dict/idf.utf8",
                         "../dict/stop_words.utf8")

print("=" * 80)
words = jieba.cut("我来到北京清华大学")
for word in words:
    print(word)

print("=" * 80)
words = jieba.cut_with_tag("我来到北京清华大学")
for word in words:
    print(word[0] + ", " + word[1])
