#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from urllib import quote
import simplejson as json

from crawler import WebCrawler
from soups import BaikeSoup
from common_keys import *
from my_utils import *

FOLDER_PREFIX = '../../../BaikeExtracter/'
LEMMA_RECORD_PATH = FOLDER_PREFIX + '{}.json'

class BaikeExtracter(object):

    def __init__(self, contents):

        if not os.path.exists(FOLDER_PREFIX):
            os.makedirs(FOLDER_PREFIX)

        soup = BaikeSoup(contents)
        soup.parse_current_page()
        soup.parse_structure()
        self.json_str = json.dumps(soup.structure, ensure_ascii=False, indent=4, sort_keys=False)
        self.lemma = soup.lemma

def main(contents):
    aBaikeExtracter = BaikeExtracter(contents)
    save_to_file(LEMMA_RECORD_PATH.format(aBaikeExtracter.lemma.encode('utf-8')), aBaikeExtracter.json_str.encode('utf-8'))

if __name__ == '__main__':
    directory = '../../../BaiduWorker/'
    for fileName in os.listdir(directory):
        if fileName.endswith('.html'):
            print ('processing {}'.format(fileName))
            with open(os.path.join(directory, fileName)) as dataFile:
                main(dataFile)

    # filePath = '../../../BaiKeWorker/苹果白粉病.html'
    # with open(filePath) as dataFile:
    #     main(dataFile)