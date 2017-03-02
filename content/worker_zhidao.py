#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import hashlib
# import requests
# import os

# from common_keys import *
# from my_utils import *

from baidubaike.crawler import WebCrawler
from baidubaike.soups import *
import os

SEARCH_QUERY = 'https://zhidao.baidu.com/search?lm=0&rn=10&fr=search&word=title: ({})&pn={}'
FOLDER_PREFIX = '../../BaiduWorker/'
ZHIDAO_RESULT_FOLDER = FOLDER_PREFIX + '{}.html'
ZHIDAO_SEARCH_RESULT_FOLDER = FOLDER_PREFIX + '_{}_{}.html'

class ZhidaoSearchSoup(BaseSoup):

    def __init__(self, contents):
        super(ZhidaoSearchSoup, self).__init__(contents)

        self.total_hits = ''
        self.hits = []

    def parse_current_page(self):
        # 获取搜索结果条数
        if self.soup.find(class_='f-lighter lh-22'):
            self.total_hits = self.soup.find(class_='f-lighter lh-22').get_text()
        for hit in self.soup.find_all('dl', class_='dl'):
            if hit.find('a'):
                url = hit.find('a')['href']
                url = url.split(".html", 1)[0]
                self.hits.append(url)

    def save_result(self):
        json_obj = {
            "total_hits": self.total_hits,
            "hits": self.hits
        }
        json_str = json.dumps(json_obj, ensure_ascii=False, indent=4, sort_keys=True)
        # save_to_file(LEMMA_RECORD_PATH, json_str.encode('utf-8'))
        print (json_str)


class ZhidaoSoup(BaseSoup):

    def __init__(self, contents, qid):
        super(ZhidaoSoup, self).__init__(contents)

        self.u_best_answer = ''
        self.u_answers = []
        self.u_qid = qid

    def save_result(self):
        json_obj = {
            "best_answer": self.u_best_answer,
            "answers": self.u_answers,
            "qid": self.u_qid
        }
        json_str = json.dumps(json_obj, ensure_ascii=False, indent=4, sort_keys=True)
        # save_to_file(LEMMA_RECORD_PATH, json_str.encode('utf-8'))
        print (json_str)

    def parse_current_page(self):
        answer_divs = self.soup.select('div.bd.answer')
        for div in answer_divs:
            if div.parent and div.parent.get('id') and 'best-answer' in div.parent['id']:
                # 最佳答案
                self.u_best_answer = self.parse_answer_div(div)
            else:
                # 其它答案
                self.u_answers.append(self.parse_answer_div(div))

    def parse_answer_div(self, div):
        child = div.find('div', class_='line content')
        if child:
            # 百度可能将答案中的文字替换成图片
            # 尝试清除可能的img标签
            for img in child.find_all('img'):
                img.decompose()
        return ''.join([text for text in child.stripped_strings])


def crawl_single_page(url):
    aWebCrawler = WebCrawler(url)
    qid = url.split('/')[-1]
    aWebCrawler.save_source_to_file(ZHIDAO_RESULT_FOLDER.format(qid + '.html'))
    soup = ZhidaoSoup(aWebCrawler.source, qid)
    soup.parse_current_page()
    soup.save_result()        

def crawl_zhidao_search(keyword, pn = 0):
    url = SEARCH_QUERY.format(keyword, pn)
    print ('process url: {}'.format(url))
    aWebCrawler = WebCrawler(url)
    aWebCrawler.save_source_to_file(ZHIDAO_SEARCH_RESULT_FOLDER.format(keyword, pn))
    soup = ZhidaoSearchSoup(aWebCrawler.source)
    soup.parse_current_page()
    soup.save_result()   

    for hit in soup.hits:
        crawl_single_page(hit)
    

if __name__ == '__main__':

    if not os.path.exists(FOLDER_PREFIX):
        os.makedirs(FOLDER_PREFIX)

    # 含有最佳答案、其它答案的页面
    url = 'https://zhidao.baidu.com/question/2117472157078581147.html'
    # 没有最佳答案的页面
    # url = 'https://zhidao.baidu.com/question/1961221172472924660.html'
    # crawl_single_page(url)

    keyword = '苹果'
    pn = 0
    crawl_zhidao_search(keyword, pn)