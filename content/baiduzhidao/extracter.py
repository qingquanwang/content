#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..baidubaike.crawler import *
# from ..baidubaike.soups import *
import os

FOLDER_PREFIX = '../../BaiduWorker/'



if __name__ == "__main__":
    print('msm')
    # __package__ = "content.baiduzhidao"
    if not os.path.exists(FOLDER_PREFIX):
        os.makedirs(FOLDER_PREFIX)
    url = 'http://www.python.org/dev/peps/pep-0366/'
    aWebCrawler = WebCrawler(url)
    print (aWebCrawler)

