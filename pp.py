import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import re
import json
from bs4 import BeautifulSoup
import os
from lxml import etree
import fire
from loguru import logger
from fake_useragent import  UserAgent
from user_header import HEADERS
import random

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")

headers = HEADERS

proxies = {}


def list_page(url):
    logger.info('crawling: %s' % url)
    resp = requests.get(url, headers=headers, proxies=proxies)
    html = etree.HTML(resp.text)
    vkeys = html.xpath('//*[@class="phimage"]/div/a/@href')
    gif_keys = html.xpath('//*[@class="phimage"]/div/a/img/@data-mediabook')
    for i in range(len(vkeys)):
        item = {}
        item['vkey'] = vkeys[i].split('=')[-1]
        item['gif_url'] = gif_keys[i]
        try:
            if 'ph' in item['vkey']:
                download(item['gif_url'], item['vkey'], 'webm')
                with open('download.txt','a') as file:
                    file.write(item['vkey'] + '\n')

        except Exception as err:
            logger.error(err)


def detail_page(url):
    s = requests.Session()
    resp = s.get(url, headers=headers, proxies=proxies)
    html = etree.HTML(resp.text)
    title = ''.join(html.xpath('//h1//text()')).strip()
    logger.info(title)

    js = html.xpath('//*[@id="player"]/script/text()')[0]
    tem = re.findall('var\\s+\\w+\\s+=\\s+(.*);\\s+var player_mp4_seek', js)[-1]
    con = json.loads(tem)

    for _dict in con['mediaDefinitions']:
        if 'quality' in _dict.keys() and _dict.get('videoUrl'):
            logger.info('%s %s' % (_dict.get('quality'), _dict.get('videoUrl')))
            logger.info('start download...')
            try:
                download(_dict.get('videoUrl'), title, 'mp4')
                break
            except Exception as err:
                logger.error(err)


def download(url, name, filetype):
    filepath = '%s/%s.%s' % (filetype, name, filetype)
    if os.path.exists(filepath):
        logger.info('this file had been downloaded :: %s' % filepath)
        return
    else:
        rep = requests.get(url, headers=headers, proxies=proxies)
        with open(filepath, 'wb') as file:
            file.write(rep.content)
        logger.info('download success :: %s' % filepath)


def run(_arg=None):
    paths = ['webm', 'mp4']
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    if _arg == 'webm':
        urls = ['https://www.pornhub.com/video?o=tr', 'https://www.pornhub.com/video?o=ht',
                'https://www.pornhub.com/video?o=mv', 'https://www.pornhub.com/video']
        for url in urls:
            list_page(url)
    elif _arg == 'mp4':
        with open('download.txt', 'r') as file:
            keys = file.readlines()
        for key in keys:
            if not key.strip():
                continue
            url = 'https://www.pornhub.com/view_video.php?viewkey=%s' % key.strip()
            logger.info('url: {}', url)
            detail_page(url)
    else:

        _str = """
        tips:
            python crawler.py webm
                - 下载热门页面的缩略图，路径为webm文件夹下
            python crawler.py mp4
                - 将下载的webm文件对应的以ph开头的文件名逐行写在download.txt中，运行该命令
                """
        logger.info(_str)
        return


logger.info('finish !')

if __name__ == '__main__':
    ua = UserAgent()
    ua.rand
    # fire.Fire(run('mp4'))