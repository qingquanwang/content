#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from urllib import quote
import simplejson as json
import csv

from crawler import WebCrawler
from soups import BaikeSoup
from common_keys import *
from my_utils import *

FOLDER_PREFIX = '../../../BaiKeWorker/'
LEMMA_PATTERN = FOLDER_PREFIX + "{}.html"
MID_FILE_PATTERN = FOLDER_PREFIX + "_{}.html"
RELATED_URL_PATTERN = 'http://baike.baidu.com/wikiui/api/zhixinmap?lemmaId={}'
MAX_DOWNLOAD_COUNT = 10
MAX_RECURSION_DEPTH = 2
MAX_RETRY = 5
BAIKE_404 = 'http://baike.baidu.com/error.html'
    
class BaikeWorker(object):

    def __init__(self, url):
        self.soup = None
        self.fetchedCount = 0
        self.loadedUrls = {}
        self.loadedLemma = []

        if not os.path.exists(FOLDER_PREFIX):
            os.makedirs(FOLDER_PREFIX)

        self.proceed(url)
        # self.save_lemma_info()

    def proceed(self, url, level = 0):
        self.fetchedCount += 1
        # print ('{} lemmas collected'.format(self.fetchedCount))
        crawler = WebCrawler(url)
        if crawler.response.url == BAIKE_404:
            print ("url: {} returns 404".format(url))
            return
        self.soup = BaikeSoup(crawler.source)
        self.soup.parse_current_page()
        lemmaName = self.soup.lemma.encode('utf-8')
        crawler.save_source_to_file(LEMMA_PATTERN.format(lemmaName))

        self.loadedUrls[url] = True
        self.loadedLemma.append(lemmaName)
        if (url != crawler.response.url):
            self.loadedUrls[crawler.response.url] = True
        
        if (self.soup.lemmaid == ID_UNSET):
            return
        tried = 0
        while True:
            relatedApi = RELATED_URL_PATTERN.format(self.soup.lemmaid)
            crawler = WebCrawler(relatedApi)
            source = crawler.response.text.encode(crawler.response.encoding)
            jsonObj = json.loads(source)
            if isinstance(jsonObj, list) == True:
                break
            else:
                tried += 1
                if tried > MAX_RETRY:
                    print ('tried 5 times but still return error, url: {}'.format(relatedApi))
                    return
                    
        level += 1
        for relatedLemma in jsonObj[0]['data']:
            if os.path.isfile(LEMMA_PATTERN.format(relatedLemma['title'].encode('utf-8'))):
                pass
            # if (relatedLemma['title'].encode('utf-8') in self.loadedLemma):
                # print('{} already downloaded, will not start download').format(relatedLemma['title'].encode('utf-8'))
            elif level > MAX_RECURSION_DEPTH:
                # print('reach max recursion depth, will not start download')
                pass
            elif self.fetchedCount > MAX_DOWNLOAD_COUNT:
                # print('reach max search count, will not start download')
                pass
            elif relatedLemma['url'] in self.loadedUrls:
                # print('{} already downloaded, will not start download').format(relatedLemma['url'])
                pass
            else:
                self.proceed(relatedLemma['url'], level)
        # self.crawler.save_source_to_file(MID_FILE_PATTERN.format(self.soup.lemmaid))

def main(url):
    aBaikeWorker = BaikeWorker(url)

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
                        main(row[1])


if __name__ == '__main__':
    # url = sys.argv[1]
    # print(url)
    # url = 'http://baike.baidu.com/item/%E8%8B%B9%E6%9E%9C%E8%85%90%E7%83%82%E7%97%85'
    # main(url)

    # directory = sys.argv[1]
    directory = '../../resources/baike/'
    readFolder(directory)