#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import requests
import os

from common_keys import *
from my_utils import *

HTTP_STATUS_OK = 200
SOURCE_PATH = 'default_htmls/'

class WebCrawler(object):

    url = None # 加载的url 可能因为重定向而与实际的url不同
    response = None
    source = None
    fileName = None

    def __init__(self, url):
        self.url = url
        self.fetch_content()

    def fetch_content(self):
        response = requests.get(self.url)
        if (response.status_code == HTTP_STATUS_OK):
            # print ('fetch url: {}, response code = {}'.format(self.url, response.status_code))
            self.source = response.text.encode(response.encoding)
        else:
            print ('faled to fetch url: {}, response code = {}'.format(self.url, response.status_code))
        self.response = response

    def save_source_to_file(self, fileName = 'unset'):
        if fileName == 'unset':
            if not os.path.exists(SOURCE_PATH):
                os.makedirs(SOURCE_PATH)
            fileName = SOURCE_PATH + md5_unicode(self.response.url) + SOURCE_EXT
        save_to_file(fileName, self.source)
        self.fileName = fileName

def main(url):
    aWebCrawler = WebCrawler(url)
    aWebCrawler.save_source_to_file()

if __name__ == '__main__':
    url = 'http://www.baidu.com/s?wd=%E8%8B%B9%E6%9E%9C%20%E7%97%85%20site%3Abaike.baidu.com'
    main(url)