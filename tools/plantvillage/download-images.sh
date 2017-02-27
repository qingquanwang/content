#!/bin/bash -x
# usage: 
#   cd imagedir
#   cat ../urls/apples/urllist | ../tools/plantvillage/download-images
xargs -n 1 -P 10 wget -nc
