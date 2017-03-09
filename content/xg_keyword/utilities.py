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


def split_process(line, search_lemmas):
    short = u''
    remain = u''

    prefix_list = [u'药用植物', u'药', u'四季', u'大', u'香', u'贴梗']
    for prefix in prefix_list:
        if line.startswith(prefix):
            line = line.replace(prefix, '', 1)
    for i in range(len(line)):
        temp = line[:(-1) * i]
        if temp in search_lemmas:
            short = temp
            remain = line.replace(short, u'')
            # print (u'在长字典项: {} 里找到短字典项: {}, 剩下: {}'.format(line, temp, remain))
            break
    if not short:
        # print(u'长字典项: {} 里没有短字典项'.format(line))
        remain = line

    return short, remain


def split_lemma(args):
    global is_debug
    is_debug = True

    containing_lemma_path = args[0]
    search_lemma_path = args[1]

    # 生成list
    search_lemmas = []
    with open(search_lemma_path, 'r') as f1:
        for line in f1:
            line = line.decode('utf-8').strip()
            search_lemmas.append(line)
    # 添加遗漏的词条:
    search_lemmas.extend([u'节瓜', u'合果芋', u'孔雀竹芋', u'李子树', u'杏树', u'杜鹃', u'枣', u'枣树', u'柿', u'桑葚', u'橙', u'油橄榄', u'洋香瓜', u'月季', u'番木瓜', u'白菜', u'紫菜', u'红菜苔', u'脐橙'])
    # ll(search_lemmas)

    with open(containing_lemma_path, 'r') as f2:
        for line in f2:
            line = line.decode('utf-8').strip()
            line = line.replace(u' ', '')
            # 删除括号
            import re
            line = re.sub(ur'\([^)]*\)', '', line)
            line = re.sub(ur'\（[^）]*\）', '', line)
            # 将含有顿号的词条分割成两个词 ·
            short1 = u''
            for symbol in [u'·', u'、']:
                if symbol in line:
                    short1 = line.split(symbol)[0]
                    line = line.split(symbol)[1]
            short, remain = split_process(line, search_lemmas)
            print('{}\t{}'.format(short.encode('utf-8'), remain.encode('utf-8')))
            if short1:
                print('{}\t{}'.format(short1.encode('utf-8'), remain.encode('utf-8')))
