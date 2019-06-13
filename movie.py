# -*- coding: utf-8 -*-
import requests
import json
import re
import os
from requests.exceptions import RequestException
import pymongo
from multiprocessing.dummy import Pool as ThreadPool
import datetime

txy_ip = '132.232.85.51'
client = pymongo.MongoClient(txy_ip)
db = client['Movie']
collection = db['Video']
american = db['American']

headers = {
    'User-Agent': 'Movie/1 CFNetwork/976 Darwin/18.2.0',
    'Content-Type': 'application/json',
    'token': 'eyJhbGciOiJIUzI1NiJ9.eyJleHQiOjE1NjEwODkxNjg5NTQsInVpZCI6MTY3MCwiaWF0IjoxNTYwMTUwMDcwODQyfQ.Vb5dla4m-6y2rt1yPYCz6g4iBlD1f0qlvICRY7VCwgU'
}

cdn_headers = {
    'User-Agent': 'AppleCoreMedia/1.0.0.16C101 (iPhone; U; CPU OS 12_1_2 like Mac OS X; zh_cn)',
    'x-playback-session-id': '9EF76EC2-4593-4804-A48E-4B99469ACC41',
}

base_url = 'http://47.91.239.32:8282'
cdn_url = 'https://cdn.35zycdn.com/'


# 将所有连接存入MongoDB
def save_to_db(data):
    if american.update({'videoUrl': data['videoUrl']}, {'$set': data}, True):
        print('保存成功')
    else:
        print('已经存在', data['videoName'])


# 查询数据库中所有的数据
def find_all_from_db():
    pool = ThreadPool()
    pool.map(get_ts_request, [item for item in collection.find()])


# 查询数据库中所有的数据
def find_one_from_db():
    data = american.find_one()
    get_ts_request(data)


# 获取首页信息
def getIndexInfo():
    url = base_url + '/openapi/indexInfo'
    param_json = {"deviceCode": "CB61E9D6-E2E1-4F88-87B4-3B64A0064C6D"}
    response = requests.post(url, data=json.dumps(param_json), headers=headers)
    jsonDict = response.json()
    classifyList = jsonDict['data']['classifyList']
    for item in classifyList:
        id = item['id']
        categoryName = item['name']
        getVideoByStarId(id, categoryName)
# for item in videoList:
#     # getDown_request(item['videoUrl'])
#     print(item['videoUrl'])


def getPages(id):
    url = base_url + '/openapi/getVideoByStarId'
    param_json = {"classifyId": id, "deviceCode": "CB61E9D6-E2E1-4F88-87B4-3B64A0064C6D"}
    response = requests.post(url, data=json.dumps(param_json), headers=headers)
    jsonDict = response.json()
    pages = jsonDict['pages']
    print(pages)
    category_video_list = []
    pool = ThreadPool()
    pool.map(getVideoByStarId, [i for i in range(1, pages + 1)])
# for i in range(1, pages+1):
#     getVideoByStarId(id, i)


# 获取视频列表
def getVideoByStarId(pageNum=1):
    print(pageNum)
    url = base_url + '/openapi/getVideoByStarId'
    param_json = {"classifyId": 3, "deviceCode": "CB61E9D6-E2E1-4F88-87B4-3B64A0064C6D", 'pageNum': pageNum}
    response = requests.post(url, data=json.dumps(param_json), headers=headers)
    jsonDict = response.json()
    videoList = jsonDict['data']
    getRealAddress_request(videoList)


# 获取视频真实地址
def getRealAddress_request(video_list):
    # video_list = getVideoByStarId(i)
    for item in video_list:
        videoUrl = item['videoUrl']
        videoName = item['videoName']
        category_name = item['tags']
        response = requests.get(videoUrl, headers=headers)
        m3u8_url = cdn_url + '/'.join(response.text.split('/')[-2:])
        getDown_request(m3u8_url, videoUrl, category_name, videoName)


# 获取所有 ts url
def getDown_request(m3u8_url, videoUrl, categor_name, video_name):
    response = requests.get(m3u8_url.strip(), headers=cdn_headers)
    content = response.text
    ts_url_list = []
    for ts_url in re.compile(r'/.*?\.ts').findall(content):
        url = cdn_url + ts_url
        ts_url_list.append(url)
    data = {
        'video_name': video_name,
        'categor_name': categor_name,
        'videoUrl': videoUrl,
        'm3u8_url': m3u8_url,
        'ts_url_list': ts_url_list
    }
    save_to_db(data)


# 下载 ts
def get_ts_request(data):
    dir_name = 'Movie/%s/%s' % (data['categor_name'].strip(), data['video_name'].strip())
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    all_ts_url = []
    for i in range(len(data['ts_url_list'])):
        item = {
            'ts_url': data['ts_url_list'][i],
            'dir_name': dir_name,
            'file_name': i
        }
        all_ts_url.append(item)
    
    print('开始下载: %s  下载文件数量: %s' % (data['video_name'], len(data['ts_url_list'])))
    start = datetime.datetime.now().replace(microsecond=0)
    pool = ThreadPool()
    pool.map(download_ts, [item for item in all_ts_url])
    end = datetime.datetime.now().replace(microsecond=0)
    print("下载完成: %s  耗时：%s" % (data['video_name'], end - start))


def download_ts(data):
    try:
        response = requests.get(data['ts_url'].strip(), headers=cdn_headers)
    except Exception as e:
        print("异常请求：%s" % e.args)
        return
    
    file_path = '%s/%s/%d.ts' % (os.path.abspath('.'), data['dir_name'], data['file_name'])
    with open(file_path, mode='ab+') as f:
        f.write(response.content)


# 合并 ts -> mp4
# def merge_ts():


if __name__ == '__main__':
    # file_path = '%s/%s' % (movie, 'Test')
    #
    # getIndexInfo()
    # pool = ThreadPool()
    # pool.map(getPages, [i for i in range(1, 9)])
    # getPages(3)
    
    # getDown_request("https://cdn.35zycdn.com/ppvod/hiptzU30.m3u8", "", "")
    # ﻿https://cdn.35zycdn.com/ppvod/UEK4ep3J.m3u8
    
    # getRealAddress_request("https://cdn.35zycdn.com/20190420/I4RhORSx/index.m3u8", 'Test')
    
    # find_all_from_db()
    
    find_one_from_db()

