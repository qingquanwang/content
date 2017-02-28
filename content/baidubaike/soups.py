#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bs4 import Tag
from bs4 import NavigableString
import simplejson as json

from my_utils import *
from common_keys import *


SOUP_PARSER = 'lxml'

def getStr(tag):
    result = u''
    for string in tag.stripped_strings:
        result += string
    return result

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
        self.structure = {}

    
    def parse_current_page(self):
        self.lemma = self.soup.h1.string

        tag = self.soup.select('div.lemmaWgt-promotion-rightPreciseAd')[0]
        self.lemmaid = tag['data-lemmaid']

    def parse_structure(self):
        soup = self.soup
        structure = {}
        # 提取词条名
        structure[J_NAME] = soup.h1.string
        # 提取每一段摘要
        summary = ''
        for para in soup.find(attrs={"label-module":'lemmaSummary'}).find_all('div'):
            summary += getStr(para)
        structure[J_SUMMARY] = summary
        # 提取基本信息
        basicInfo = {}
        basicInfoKeys = soup.find_all('dt', class_='basicInfo-item name')
        basicInfoValues = soup.find_all('dd', class_='basicInfo-item value')
        for i in range(len(basicInfoKeys)):
            key = getStr(basicInfoKeys[i])
            value = getStr(basicInfoValues[i])
            basicInfo[norm_unicode(key)] = norm_unicode(value)
        structure[J_BASIC_INFO] = basicInfo
        # 提取h2
        h2Info = {}
        for h2 in soup.find_all('div', class_='para-title level-2'):
            self.parse_h2(h2, h2Info)
        structure[J_H2_INFO] = h2Info
        self.structure = structure

    def parse_h2(self, tag, dic):
        title = ''
        for child in tag.find('h2'):
            if isinstance(child, NavigableString):
                title += child
        nextTag = tag
        contents = ''
        while True:
            nextTag = nextTag.find_next_sibling('div')
            if nextTag.get('label-module') == None or nextTag.get('label-module') != 'para':
                break
            contents += getStr(nextTag)
        dic[title] = contents

def test_baidu_soup(contents):
    aBaiduSoup = BaiduSoup(contents)
    aBaiduSoup.parse_current_page()
    aBaiduSoup.save_lemmas()

if __name__ == '__main__':
    with open('htmls/643ea1105aca7c5ef8b853e5c5817d97.html', 'r') as test:
        test_baidu_soup(test)



