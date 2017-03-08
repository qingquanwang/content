#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import simplejson as json

from common_keys import *
from my_utils import *

is_debug = False
JSON_EXT = u'.json'
ALIAS_LIST = [u'别称']
plants = []
diseases = []


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
    else:
        print(u'll未处理的类型: {}'.format(type(msg)))


def lj(json_content):
    json_str = json.dumps(json_content, ensure_ascii=False, indent=4, sort_keys=False)
    ll(json_str)


def extract_folder(directory, ext, handler):
    for fileName in os.listdir(directory):
        if fileName.endswith(ext):
            with open(os.path.join(directory, fileName)) as dataFile:
                handler(dataFile)


def parse_plant_json(contents):
    json_obj = json.load(contents)
    candidates = []
    # 读取name
    if J_NAME not in json_obj:
        le(u'json中不存在name字段', u'检查{}'.format(contents.name))
    candidates.append(json_obj[J_NAME])
    # 读取别名
    if J_BASIC_INFO not in json_obj:
        le(u'json中不存在basic_info字段', u'检查{}'.format(contents.name))
    lj(json_obj[J_BASIC_INFO])
    for alias in ALIAS_LIST:
        if alias in json_obj[J_BASIC_INFO]:
            hits = json_obj[J_BASIC_INFO][alias]
            delimiters = [u'、', u'，', u'。']
            for delimiter in delimiters:
                hits = hits.replace(delimiter, ' ')
            hits = hits.split()
            # hits = filter(None, re.split(ur'(、|，|。|,| )\s*', hits))  # 中文顿号，空格
            ll(hits)
            for hit in hits:
                if hit not in candidates:
                    candidates.append(hit)
    # ll(candidates)
    # 防重复处理
    for candidate in candidates:
        if candidate in plants:
            # print ('plants: ')
            # print (plants)
            lw(u'出现重复的植物名: {}'.format(candidate), u'检查{}'.format(contents.name))
        else:
            plants.append(candidate)


def save_result(out_path, file_name, keywords):
    ll(keywords)
    contents = u''
    for kw in keywords:
        contents += kw + u'\n'
    save_to_file(os.path.join(out_path, file_name), contents.encode(encoding='utf-8'))


def plant_keyword(args):
    # print('input: {}, output: {}'.format(os.path.abspath(in_path), os.path.abspath(out_path)))
    extract_folder(args[0], JSON_EXT, parse_plant_json)
    save_result(args[1], u'植物名.txt', plants)


def plant_keyword_test(args):
    global is_debug
    is_debug = True
    with open(args[0]) as dataFile:
        parse_plant_json(dataFile)
    save_result(args[1], u'植物名.txt', plants)


def parse_disease_json(contents):
    json_obj = json.load(contents)
    candidates = []
    # 读取name
    if J_NAME not in json_obj or not json_obj[J_NAME] or not json_obj[J_NAME].endswith(u'病'):
        le(u'json中不存在name字段或为空或不以病结尾', u'检查{}'.format(contents.name))
        return
    candidates.append(json_obj[J_NAME])
    # 读取别名
    if J_BASIC_INFO not in json_obj:
        le(u'json中不存在basic_info字段', u'检查{}'.format(contents.name))
    lj(json_obj[J_BASIC_INFO])
    for alias in ALIAS_LIST:
        if alias in json_obj[J_BASIC_INFO]:
            hits = json_obj[J_BASIC_INFO][alias]
            delimiters = [u'、', u'，', u'。']
            for delimiter in delimiters:
                hits = hits.replace(delimiter, ' ')
            hits = hits.split()
            # hits = filter(None, re.split(ur'(、|，|。|,| )\s*', hits))  # 中文顿号，空格
            ll(hits)
            for hit in hits:
                if hit not in candidates:
                    candidates.append(hit)
    # ll(candidates)
    # 防重复处理
    for candidate in candidates:
        if candidate in plants:
            lw(u'出现重复的病名: {}'.format(candidate), u'检查{}'.format(contents.name))
        else:
            diseases.append(candidate)


def disease_keyword(args):
    extract_folder(args[0], JSON_EXT, parse_disease_json)
    save_result(args[1], u'病名.txt', diseases)


def disease_keyword_test(args):
    global is_debug
    is_debug = True
    with open(args[0]) as dataFile:
        parse_disease_json(dataFile)
    save_result(args[1], u'病名.txt', diseases)
