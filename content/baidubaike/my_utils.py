#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os


def save_to_file(fileName, fileContents):
    filePath = os.path.dirname(fileName)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    with open(fileName, 'w') as f:
        f.write(fileContents)
    print ('file saved to {}'.format(fileName))


def md5_unicode(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def norm_unicode(str):
    result = str.encode('utf-8').strip()
    result = result.replace(' ', '')
    return result


def mkdir_recursive(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def init_paths(root):
    if not root.endswith('/'):
        root += '/'
    raw_search_path = root + 'raw/baidu/search-diseases/'
    raw_question_path = root + 'raw/baidu/zhidao-diseases/'
    json_path = root + 'json/baidu/zhidao-diseases/'
    mkdir_recursive(root, raw_search_path, raw_question_path, json_path)
    raw_search_file = raw_search_path + '_{}_{}.html'
    raw_question_file = raw_question_path + '{}.html'
    json_file = json_path + '{}.json'

    return raw_search_file, raw_question_file, json_file
