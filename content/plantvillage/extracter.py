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
            disease_sec_num = len(disease_secs)
            if disease_sec_num > 0:
                dobj['symptoms'] = content_norm(disease_secs[0].get_text())
            if disease_sec_num > 1:
                dobj['comments'] = content_norm(disease_secs[1].get_text())
            if disease_sec_num > 2:
                dobj['management'] = content_norm(disease_secs[2].get_text())
            res['diseases'].append(dobj)
    return res
def extract_question_page(file):
    res = None
    with open(file, 'r') as fd:
        res = []
        p = json.load(fd)
        for post in p['posts']:
            post_obj = {}
            post_obj['title'] = content_norm(post['title'])
            post_obj['text'] = content_norm(post['text'])
            if len(post['post_images']) > 0:
                post_obj['images'] = []
                for post_image in post['post_images']:
                    post_obj['images'].append(post_image['url'])
            res.append(post_obj)
    return res


def main():
    directory = sys.argv[1]
    topics_summary = "plant-village-topics-summary"
    topics = {}
    questions_summary = "plant-village-questions-summary"
    questions = {}
    if len(sys.argv) > 2:
        topic_summary = sys.argv[2]
    if len(sys.argv) > 3:
        question_summary = sys.argv[3]
    for subdir in os.listdir(directory):
        topic= os.path.split(subdir)[1]
        topic_dir = os.path.join(directory, subdir)
        topic_page = os.path.join(topic_dir, "diseases_and_pests_description_uses_propagation")
        question_page = os.path.join(topic_dir, "questions")
        if os.path.exists(topic_page):
            topics[topic] = extract_topic_page(topic_page)
        if os.path.exists(question_page):
            pp.pprint(question_page)
            questions[topic] = extract_question_page(question_page)
            pp.pprint(questions[topic])

    with open(topics_summary, 'w') as topics_summary_fd:
        topics_summary_fd.write(json.dumps(topics, indent=2).encode('utf-8'))
    
    with open(questions_summary, 'w') as questions_summary_fd:
        questions_summary_fd.write(json.dumps(questions, indent=2).encode('utf-8'))
if __name__ == '__main__':
    main()
