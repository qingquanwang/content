#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json

from soups import BaikeSoup
from common_keys import *
from my_utils import *
import argparse

FOLDER_PREFIX = '../../../BaikeExtracter/'
FOLDER_PREFIX_BOLD = '../../../BaikeExtracter/bold/'
LEMMA_RECORD_PATH = FOLDER_PREFIX + '{}.json'
LEMMA_RECORD_PATH_BOLD = FOLDER_PREFIX_BOLD + '{}.json'


class BaikeExtracter(object):

    def __init__(self, contents, is_bold=False):

        if not os.path.exists(FOLDER_PREFIX):
            os.makedirs(FOLDER_PREFIX)
        if not os.path.exists(FOLDER_PREFIX_BOLD):
            os.makedirs(FOLDER_PREFIX_BOLD)

        soup = BaikeSoup(contents, is_bold)
        soup.parse_current_page()
        soup.parse_structure()
        if (len(soup.structure) == 0):
            self.lemma = ''
        else:
            self.json_str = json.dumps(soup.structure, ensure_ascii=False, indent=4, sort_keys=False)
            self.lemma = soup.lemma


def main(contents, is_bold=False):
    aBaikeExtracter = BaikeExtracter(contents, is_bold)
    if (aBaikeExtracter.lemma == ''):
        return
    fileName = aBaikeExtracter.lemma.encode('utf-8')
    fileName = fileName.replace('/', '__')
    if is_bold:
        save_to_file(LEMMA_RECORD_PATH_BOLD.format(fileName), aBaikeExtracter.json_str.encode('utf-8'))
    else:
        save_to_file(LEMMA_RECORD_PATH.format(fileName), aBaikeExtracter.json_str.encode('utf-8'))


def extract_folder(directory, is_bold):
    for fileName in os.listdir(directory):
        if fileName.endswith('.html'):
            print ('processing {}'.format(fileName))
            with open(os.path.join(directory, fileName)) as dataFile:
                main(dataFile, is_bold)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('out_path', help='指定输出.json文件的根目录')
    parser.add_argument('-in_path', nargs='?', const='../../../data/raw/baidu/baike-plants/', help='需要提取的html路径，默认是../../../data/raw/baidu/baike-plants/')
    parser.add_argument('-single', help='提取指定位置的html')
    args = parser.parse_args()
    if not args.out_path.endswith('/'):
        arg.out_path += '/'
    LEMMA_RECORD_PATH_BOLD = args.out_path + '{}.json'

    if args.single:
        with open(args.single) as dataFile:
            main(dataFile, True)
    elif args.in_path:
        # 提取页面去除b tag
        # extract_folder('../../../BaiduWorker/', False)
        # 提取页面保留b tag
        extract_folder(in_path, True)
