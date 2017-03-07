#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fix_path
import argparse
import xg_keyword.generator

functions = {'plant': xg_keyword.generator.plant_keyword,
             'plant_test': xg_keyword.generator.plant_keyword_test}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='生成关键词', usage='''
        植物: python main.py plant ../../data/json/baidu/baike-plants/ ../../output/
        植物test: python main.py plant_test ../../data/json/baidu/baike-plants/芭蕉.json ../../output/
        ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('type', help='指定生成的关键词类型: plant')
    parser.add_argument('in_path', help='指定输入根目录')
    parser.add_argument('out_path', help='指定输出关键词.txt文件的根目录')
    args = parser.parse_args()
    if args.type not in functions:
        print('请输入有效的关键词类型，参见-h')

    func = functions[args.type]
    func([args.in_path, args.out_path])
