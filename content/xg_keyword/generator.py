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


def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


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


def save_plant(out_path):
    ll(plants)
    contents = u''
    for plant in plants:
        contents += plant + u'\n'
    save_to_file(os.path.join(out_path, u'植物名.txt'), contents.encode(encoding='utf-8'))


def plant_keyword(args):
    in_path = args[0].decode('utf-8')
    out_path = args[1].decode('utf-8')
    # print('input: {}, output: {}'.format(os.path.abspath(in_path), os.path.abspath(out_path)))
    extract_folder(in_path, JSON_EXT, parse_plant_json)
    save_plant(out_path)


def plant_keyword_test(args):
    file_path = args[0].decode('utf-8')
    out_path = args[1].decode('utf-8')
    global is_debug
    is_debug = True
    with open(file_path) as dataFile:
        parse_plant_json(dataFile)
    save_plant(out_path)
