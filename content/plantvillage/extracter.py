# -*- coding: utf-8 -*-
# extract topic page/question to json-structered information

from bs4 import BeautifulSoup
import re
import os, sys
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)


def content_norm(str):
    tmp = str.strip().lower()
    tmp1 = re.sub(r'\s+',' ', tmp)
    return re.sub(r'\n+',' ', tmp1)

def extract_topic_page(file):
    res = None
    with open(file, 'r') as fd:
        res = {}
        page = BeautifulSoup(fd, 'lxml')
        res['topic_name'] = content_norm(page.select('h1[class="topic-name"]')[0].get_text())
        res['latin_name'] = content_norm(page.select('em[class="topic-description"]')[0].get_text())
        infos = page.select('p[class="info-description"]')
        num = len(infos)
        res['desc'] = content_norm(infos[0].get_text())
        res['use'] = content_norm(infos[1].get_text())
        res['propagation'] = content_norm(infos[2].get_text())
        res['diseases'] = []
        diseases = page.select('div.disease')
        for d in diseases:
            dobj = {}
            title_sec = d.select('h3[class="disease-title"]')[0]
            dobj['label'] = content_norm(title_sec.select('span.label')[0].get_text())
            for span_tmp in title_sec.select('span'):
                span_tmp.extract()
            dobj['title'] = content_norm(title_sec.get_text())
            disease_secs = d.select('p')
            dobj['symptoms'] = content_norm(disease_secs[0].get_text())
            dobj['comments'] = content_norm(disease_secs[1].get_text())
            dobj['management'] = content_norm(disease_secs[2].get_text())
            res['diseases'].append(dobj)
    return res
def extract_question_page(file):
    return


def main():
    file = sys.argv[1]
    print json.dumps(extract_topic_page(file), indent=2).encode('utf-8')
    #pp.pprint(tmp)
if __name__ == '__main__':
    main()
