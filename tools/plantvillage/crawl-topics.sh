#!/bin/bash -x
# usage:
#   cd data
#   ./crawl-topic.sh
wget -k -np -c https://www.plantvillage.org/en/topics
cat topics | grep topic-square-link | grep -v topic-square-description | sed -e 's/.*href="//g' | sed -e 's/".*$//g' | sort | uniq | xargs -n 1 -P 10 wget -k -np -c -p -L
cat topics | grep topic-square-questions | sed -e 's/.*href="//g' | sed -e 's/".*$//g' | sort | uniq | xargs -n 1 -P 10 wget -k -np -c -p -L
rm topics
python ../../content/plantvillage/extracter.py ./www.plantvillage.org/en/topics/
