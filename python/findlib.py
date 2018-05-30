# encoding: utf-8


import os
import sys
from platform import *


class CppJieBaLibraryNotFound(Exception):
    pass


def find_lib_path(user_path = None):
    cdll_names = {
        'Darwin': 'cppjieba.dylib',
        'Linux': 'cppjieba.so',
    }

    curr_path = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))

    dll_path = [user_path] if user_path else []

    dll_path.extend([curr_path,
                     os.path.join(curr_path, 'lib'),
                     os.path.join(curr_path, '../'),
                     os.path.join(curr_path, '../lib/'),
                     os.path.join(curr_path, '../../'),
                     os.path.join(curr_path, '../../lib/'),
                     os.path.join(sys.prefix, 'lib'),
                     os.path.join(sys.prefix, 'lib64')])

    dll_path = [os.path.join(p, cdll_names[system()]) for p in dll_path]
    lib_path = [p for p in dll_path if os.path.exists(p) and os.path.isfile(p)]

    if not lib_path:
        raise CppJieBaLibraryNotFound('Cannot find CppJieBa Library in the path: \n' + ('\n'.join(dll_path)))
    return lib_path
