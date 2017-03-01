#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from urllib import quote
import simplejson as json
import csv

from crawler import WebCrawler
from soups import BaiduSoup
from common_keys import *
from my_utils import *


# SEARCH_QUERY = 'http://www.baidu.com/s?wd={}%20site%3Abaike.baidu.com&pn={}'
SEARCH_QUERY = 'http://www.baidu.com/s?wd=site%3A(baike.baidu.com)%20title%3A%20({}%20(病))&pn={}'
LEMMAS_EVERY_PAGE = 10
MAX_LEMMA_COUNT = 9
FOLDER_PREFIX = '../../../BaiduWorker/'
BAIDU_RESULT_FOLDER = FOLDER_PREFIX + '_{}.html'
LEMMA_RECORD_PATH = FOLDER_PREFIX + '_lemmas.json'
LEMMA_PATTERN = FOLDER_PREFIX + "{}.html"
QUERY_PATTERN = '{} 病'

class BaiduWorker(object):

    def __init__(self, keyword):
        self.keyword = keyword
        self.totalDic = {}
        self.totalLemmas = []
        self.crawler = None
        self.soup = None
        self.fetchedCount = 0

        if not os.path.exists(FOLDER_PREFIX):
            os.makedirs(FOLDER_PREFIX)

        self.proceed()
        self.save_lemma_info()

    def proceed(self):
        while True:
            self.crawler = WebCrawler(self.get_url())
            # self.crawler.save_source_to_file(BAIDU_RESULT_FOLDER.format(self.fetchedCount))
            self.soup = BaiduSoup(self.crawler.source)
            self.soup.parse_current_page()
            # 试图寻找交集
            for newLemma in self.soup.lemmas:
                duplicated = 0
                if md5_unicode(newLemma[LEMMA_NAME]) in self.totalDic:
                    print ('find duplicated lemma: {}, skip saving'.format(newLemma[LEMMA_NAME].encode('utf-8')))
                    ++duplicated
                else:
                    self.save_lemma_page(newLemma)
                    self.totalLemmas.append(newLemma)
                    self.totalDic[md5_unicode(newLemma[LEMMA_NAME])] = True
                if duplicated == LEMMAS_EVERY_PAGE:
                    print ('find 10 duplicated items, return to 1st page, stop crawling')
                    return
                if len(self.totalLemmas) > MAX_LEMMA_COUNT:
                    print ('over max lemma count, stop crawling')
                    return
            if (len(self.soup.lemmas) < LEMMAS_EVERY_PAGE):
                print('search results less than 10, stop searching')
                return

            self.fetchedCount += LEMMAS_EVERY_PAGE

    def save_lemma_page(self, lemma):
        # print (lemma[LEMMA_URL])
        self.crawler = WebCrawler(lemma[LEMMA_URL])
        self.crawler.save_source_to_file(LEMMA_PATTERN.format(lemma[LEMMA_NAME].encode('utf-8')))

    def save_lemma_info(self):
        json_str = json.dumps(self.totalLemmas, ensure_ascii=False, indent=4, sort_keys=True)
        save_to_file(LEMMA_RECORD_PATH, json_str.encode('utf-8'))

    def get_url(self):
        url = SEARCH_QUERY.format(quote(self.keyword), self.fetchedCount)
        print ('fetch baidu search url: {}'.format(url))
        return url

def readFolder(directory):
    for fileName in os.listdir(directory):
        if fileName.endswith('.csv'):
            print ('processing {}'.format(fileName))
            with open(os.path.join(directory, fileName)) as csvFile:
                spamreader = csv.reader(csvFile)
                for row in spamreader:
                    if os.path.isfile(LEMMA_PATTERN.format(row[0])):
                        print('already downloaded lemma: {}'.format(row[0]))
                    else:
                        main(row[0])

def main(keyword):
    aBaiduWorker = BaiduWorker(keyword)
    

if __name__ == '__main__':
    # keyword = '神秘果'
    # main(keyword)

    directory = '../../resources/baike/'
    readFolder(directory)