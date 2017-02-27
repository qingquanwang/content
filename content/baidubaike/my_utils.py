#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def save_to_file(fileName, fileContents):
    with open(fileName, 'w') as f:
        f.write(fileContents)
    print ('file saved to {}'.format(fileName))

def md5_unicode(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()