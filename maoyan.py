#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import re 
import json

def get_one_page(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
    
def parse_one_page(html):
    pattern = re.co mpile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
    +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
    +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }

# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        #字典转字符串
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
    # parse_one_page(html)

if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])