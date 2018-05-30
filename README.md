# cppjiebapy

在 [cjieba](https://github.com/yanyiwu/cjieba) 的基础上做了封装，并增加了 `CutWithTag` 方法.

使用 Python `ctypes` module 访问相关函数

## Build

~~~
mkdir build
cd build
cmake ..
make -j
~~~

~~~
# For testing
python ../test/test.py

~~~


## Usage


~~~
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
~~~

### Result 

~~~
===========================
我
来到
北京
清华大学
===========================
我, r
来到, v
北京, ns
清华大学, nt
~~~
