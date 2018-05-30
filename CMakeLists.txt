cmake_minimum_required(VERSION 2.8.7)
project(cppjieba C CXX)
enable_testing()
set(CMAKE_MACOSX_RPATH 1)

find_path(CPPJIEBA_INCLUDE_DIR NAMES cppjieba/Jieba.hpp)
include_directories(${CPPJIEBA_INCLUDE_DIR})

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -std=c++11 -O3 -Wall -fPIC")

set(LIB_TIANGAN_SRC
    lib/jieba.cpp)

add_library(cppjieba SHARED
            ${LIB_TIANGAN_SRC})

set_target_properties(cppjieba PROPERTIES
                      OUTPUT_NAME "cppjieba"
                      PREFIX      "")

