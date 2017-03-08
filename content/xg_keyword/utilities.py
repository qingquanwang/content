#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
import simplejson as json
import operator

is_debug = False


def le(error, info):
    print (u'error: {}, info: {}'.format(error, info))


def lw(error, info):
    print (u'warning: {}, info: {}'.format(error, info))


def ll(msg):
    if not is_debug:
        return
    if isinstance(msg, list):
        print(u'list: [{}]'.format(u','.join(msg)))
    elif isinstance(msg, str):
        print(msg)
    elif isinstance(msg, unicode):
        print(msg)
    # elif isinstance(msg, Counter):
    #     result = u'{%s}'
    #     parts = [u'%s: %s' % (unicode(key), unicode(value)) for key, value in msg.items()]
    #     print(result % u', '.join(parts))
    # elif isinstance(msg, class_or_type_or_tuple)
    else:
        print(u'll未处理的类型: {}'.format(type(msg)))


def lj(json_content):
    json_str = json.dumps(json_content, ensure_ascii=False, indent=4, sort_keys=False)
    ll(json_str)


def cal_freq(args):
    global is_debug
    is_debug = True

    keyword_files_path = args[0]
    print(keyword_files_path)
    # 生成关键词字典
    keyword_dic = {}
    for fileName in os.listdir(keyword_files_path):
        if fileName.endswith(u'.txt'):
            with open(os.path.join(keyword_files_path, fileName)) as dataFile:
                for line in dataFile:
                    line = line.decode('utf-8').strip()
                    keyword_dic[line] = True
    # 统计词频
    file_path = args[1]
    freq_dic = defaultdict(lambda: 0)
    with open(file_path, 'r') as data_file:
        for line in data_file:
            line = line.decode('utf-8')
            words = line.split()
            for word in words:
                if word not in keyword_dic:
                    freq_dic[word] += 1

    sorted_freq_dic = sorted(freq_dic.items(), key=operator.itemgetter(1))
    for pair in sorted_freq_dic:
        print u'{} : {}'.format(pair[0], pair[1])
