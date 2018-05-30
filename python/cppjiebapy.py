# encoding: utf-8


from ctypes import *
from findlib import find_lib_path


class _JiebaHandle(Structure):
    pass


class _JiebaWordList(Structure):
    _fields_ = [("word", c_char_p),
                ("len", c_ulong)]


class _CJiebaWordWithTag(Structure):
    _fields_ = [("word", c_char_p),
                ("len", c_ulong),
                ("tag", c_char * 0)
                ]


class JieBaDLL:
    def __init__(self, lib_path):
        self.dll = CDLL(lib_path)

        self.NewJieba = self.dll.NewJieba
        self.NewJieba.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.NewJieba.restype = POINTER(_JiebaHandle)

        self.FreeJieba = self.dll.FreeJieba
        self.FreeJieba.argtypes = [POINTER(_JiebaHandle)]
        self.FreeJieba.restype = None

        self.Cut = self.dll.Cut
        self.Cut.argtypes = [POINTER(_JiebaHandle), c_char_p, c_ulong]
        self.Cut.restype = POINTER(_JiebaWordList)

        self.FreeWords = self.dll.FreeWords
        self.FreeWords.argtypes = [POINTER(_JiebaWordList)]
        self.FreeWords.restype = None

        self.CutWithTag = self.dll.CutWithTag
        self.CutWithTag.argtypes = [POINTER(_JiebaHandle), c_char_p, c_ulong]
        self.CutWithTag.restype = POINTER(_CJiebaWordWithTag)

        self.FreeWordTag = self.dll.FreeWordTag
        self.FreeWordTag.argtypes = [POINTER(_CJiebaWordWithTag)]
        self.FreeWordTag.restype = None

    def create_jieba(self, dict_path, hmm_path, user_dict, idf_path, stop_word_path):
        return JieBa(self.NewJieba(dict_path, hmm_path, user_dict, idf_path, stop_word_path), self)


class JieBa(object):
    def __init__(self, impl, DLL):
        self.impl = impl
        self.DLL = DLL

    def __del__(self):
        self.DLL.FreeJieba(self.impl)

    def cut(self, text):
        _words = self.DLL.Cut(self.impl, text, len(text))
        words = []
        for word in _words:
            if word.len == 0:
                break
            words.append(word.word[0:word.len])
        self.DLL.FreeWords(_words)
        return words

    def cut_with_tag(self, text):
        _words = self.DLL.CutWithTag(self.impl, text, len(text))
        words = []

        current = _words
        while True:
            length = current.contents.len
            if length == 0:
                break
            word = current.contents.word[0:length]

            ptr = cast(current, POINTER(c_char))
            void_p = cast(ptr, c_voidp).value + sizeof(_CJiebaWordWithTag)
            tag_ptr = cast(void_p, c_char_p)
            tag = tag_ptr.value
            words.append((word, tag))

            ptr = cast(current, POINTER(c_char))
            void_p = cast(ptr, c_voidp).value + sizeof(_CJiebaWordWithTag) + len(tag) + 1
            current = cast(void_p, POINTER(_CJiebaWordWithTag))

        self.DLL.FreeWordTag(_words)
        return words


def load_lib(user_path = None):
    libs = find_lib_path(user_path)
    lib = JieBaDLL(libs[0])
    return lib

