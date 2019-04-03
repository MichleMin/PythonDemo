#!/usr/bin/env python3
# coding:utf-8
import pymongo
import requests
from bson import binary
from lxml import html
import os
import time
from multiprocessing.dummy import Pool

from config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]


def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headersx


# 获取主页列表
def getPage(pageNum):
    baseUrl = 'https://www.mzitu.com/page/{}'.format(pageNum)
    selector = html.fromstring(requests.get(baseUrl).content)
    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
        print(i)
    return urls


# 图片链接列表， 标题
# url是详情页链接
def getPiclink(url):
    sel = html.fromstring(requests.get(url).content)
    # 图片总数
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    # 文件夹格式
    dirName = u"【{}P】{}".format(total, title)
    # # 新建文件夹
    os.mkdir(dirName)

    n = 1
    images = []
    for i in range(int(total)):
        # 每一页
        try:
            link = '{}/{}'.format(url, i + 1)
            s = html.fromstring(requests.get(link).content)
            # 图片地址在src标签中
            jpgLink = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            # print(jpgLink)
            # 文件写入的名称：当前路径／文件夹／文件名
            filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, n)
            print(u'开始下载图片:第%s张' % (i+1))
            # db = requests.get(jpgLink, headers=header(jpgLink)).content
            # images.append(binary.Binary(db))
            # url = requests.get(jpgLink, headers=header(jpgLink)).text
            # print(jpgLink)
            with open(filename, "wb+") as jpg:
                jpg.write(requests.get(jpgLink, headers=header(jpgLink)).content)
        except:
            pass
    # result = {
    #     'title': title,
    #     'images': images,
    #     'url': url
    # }
    # save_to_mongo(result)


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False


if __name__ == '__main__':
    # getPage(1)
    # url = 'http://www.meizitu.com/a/5555.html'
    # getPiclink(url)
    # for i in range(1):
    for i in range(2):
        p = getPage(i)
        pool = Pool()
        pool.map(getPiclink, p)
