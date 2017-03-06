#!/usr/bin/env python
# -*- coding: utf-8 -*-

import simplejson as json
import csv
import argparse

from crawler import WebCrawler
from soups import BaikeSoup
from common_keys import *
from my_utils import *

FOLDER_PREFIX = '../../../BaiKeWorker/'
FOLDER_BOLD = FOLDER_PREFIX + 'bold/'
LEMMA_PATTERN = FOLDER_PREFIX + "{}.html"
LEMMA_PATTERN_WITH_BOLD = ''
MID_FILE_PATTERN = FOLDER_PREFIX + "_{}.html"
RELATED_URL_PATTERN = 'http://baike.baidu.com/wikiui/api/zhixinmap?lemmaId={}'
MAX_DOWNLOAD_COUNT = 10
MAX_RECURSION_DEPTH = 2
MAX_RETRY = 5
BAIKE_404 = 'http://baike.baidu.com/error.html'


class BaikeWorker(object):

    def __init__(self, url, download_related=True):
        self.soup = None
        self.download_related = download_related
        self.fetchedCount = 0
        self.loadedUrls = {}
        self.loadedLemma = []

        if not os.path.exists(FOLDER_PREFIX):
            os.makedirs(FOLDER_PREFIX)
        if not os.path.exists(FOLDER_BOLD):
            os.makedirs(FOLDER_BOLD)

        self.proceed(url)
        # self.save_lemma_info()

    def proceed(self, url, level=0):
        self.fetchedCount += 1
        # print ('{} lemmas collected'.format(self.fetchedCount))
        crawler = WebCrawler(url)
        if crawler.response.url == BAIKE_404:
            print ("url: {} returns 404".format(url))
            return
        self.soup = BaikeSoup(crawler.source)
        self.soup.parse_current_page()
        lemmaName = self.soup.lemma.encode('utf-8')

        if not self.download_related:
            crawler.save_source_to_file(LEMMA_PATTERN_WITH_BOLD.format(lemmaName))
            return
        else:
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
            if isinstance(jsonObj, list):
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


def download_lemma_only(url):
    aBaikeWorker = BaikeWorker(url, False)


def readFolder(directory, is_bold=False):
    for fileName in os.listdir(directory):
        if fileName.endswith('.csv'):
            print ('processing {}'.format(fileName))
            with open(os.path.join(directory, fileName)) as csvFile:
                spamreader = csv.reader(csvFile)
                for row in spamreader:
                    if os.path.isfile(LEMMA_PATTERN.format(row[0])):
                        print('already downloaded lemma: {}'.format(row[0]))
                    else:
                        if is_bold:
                            download_lemma_only(row[1])
                        else:
                            main(row[1])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-path', help='指定下载的.html和.json文件的下载根目录，默认是../../data/')
    parser.add_argument('-csv', nargs='?', const='../../resources/baike/', help='指定csv读取路径，从csv中加载url，默认：../../resources/baike/')
    parser.add_argument('-url', help='指定百度百科页的url，例如http://baike.baidu.com/item/软件')
    args = parser.parse_args()

    if args.path:
        FOLDER_PREFIX = args.path
    if not FOLDER_PREFIX.endswith('/'):
        FOLDER_PREFIX += '/'
    mkdir_recursive(FOLDER_PREFIX)
    LEMMA_PATTERN_WITH_BOLD = FOLDER_PREFIX + "raw/baidu/baike-plants/{}.html"

    if args.csv:
        # 从csv中加载要下载的页
        readFolder(args.csv, True)
    elif args.url:
        # 仅下载百度百科页，保留b tag用
        url = 'http://baike.baidu.com/item/%E4%B8%89%E8%89%B2%E5%A0%87/200112'
        download_lemma_only(args.url)
    else:
        print('没有输入有效的参数')
