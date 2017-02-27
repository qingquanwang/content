#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4 import Tag
import simplejson as json

import my_utils
from common_keys import *


SOUP_PARSER = 'lxml'

class BaseSoup(object):

    def __init__(self, contents):
        self.soup = BeautifulSoup(contents, SOUP_PARSER)

class BaiduSoup(BaseSoup):

    SEARCH_RESULT_PATTERN = 'div.c-container'
    URL_TAG = 'mu'

    def __init__(self, contents):
        super(BaiduSoup, self).__init__(contents)
        self.lemmas = []

    def parse_current_page(self):
        searchResultTags = self.soup.select(self.SEARCH_RESULT_PATTERN)
        for result in searchResultTags:
            lemma = self.get_lemma_info(result)
            self.lemmas.append(lemma)

    # <a target="_blank" href='xxxx'><em>\u82f9\u679c</em>\u9ed1\u70b9<em>\u75c5</em>_\u767e\u5ea6\u767e\u79d1</a>
    def get_lemma_info(self, tag):
        aTag = tag.a
        lemma = {}
        name = ''
        hit = ''
        for child in aTag:
            if isinstance(child, Tag):
                hit += str(child)
            else:
                hit += child.string.encode('utf-8')
            name += child.string
        # 苹果功效_百度百科 
        name = name.rsplit('_', 1)[0]
        lemma[LEMMA_NAME] = name
        lemma[LEMMA_HIT] = hit
        lemma[LEMMA_URL] = tag.a['href']
        return lemma

class BaikeSoup(BaseSoup):

    def __init__(self, contents):
        super(BaikeSoup, self).__init__(contents)

        self.lemma = None
        self.lemmaid = None

    
    def parse_current_page(self):
        self.lemma = self.soup.h1.string

        tag = self.soup.select('div.lemmaWgt-promotion-rightPreciseAd')[0]
        self.lemmaid = tag['data-lemmaid']



def test_baidu_soup(contents):
    aBaiduSoup = BaiduSoup(contents)
    aBaiduSoup.parse_current_page()
    aBaiduSoup.save_lemmas()

if __name__ == '__main__':
    with open('htmls/643ea1105aca7c5ef8b853e5c5817d97.html', 'r') as test:
        test_baidu_soup(test)



