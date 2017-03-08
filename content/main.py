#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fix_path
import argparse
import xg_keyword.generator
import xg_keyword.utilities

functions = {'plant': xg_keyword.generator.plant_keyword,
             'plant_test': xg_keyword.generator.plant_keyword_test,
             'disease': xg_keyword.generator.disease_keyword,
             'disease_test': xg_keyword.generator.disease_keyword_test,
             'cal_freq': xg_keyword.utilities.cal_freq,
             }

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='生成关键词', usage='''
        植物: python main.py plant ../../data/json/baidu/baike-plants/ ../../output/
        植物test: python main.py plant_test ../../data/json/baidu/baike-plants/芭蕉.json ../../output/
        病: python main.py disease ../../data/json/baidu/baike-diseases/ ../../output/
        病test: python main.py disease_test ../../data/json/baidu/baike-diseases/枣缩果病.json ../../output/
        计算词频: python main.py cal_freq ../../output/ ../../content/resources/baike/keyords/zhidao_seg.txt
        ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('type', help='指定生成的关键词类型: plant')
    parser.add_argument('in_path', help='指定输入根目录')
    parser.add_argument('out_path', help='指定输出关键词.txt文件的根目录')
    args = parser.parse_args()
    if args.type not in functions:
        print('请输入有效的关键词类型，参见-h')

    func = functions[args.type]
    func([args.in_path.decode('utf-8'), args.out_path.decode('utf-8')])
