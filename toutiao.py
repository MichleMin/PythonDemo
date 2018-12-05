from urllib.parse import urlencode

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import json
import re


#抓取索引
def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.20 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None

def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    # print('结果:', soup.get_text)
    title = soup.select('title')[0].get_text()
    # print(title)
    image_pattern = re.compile('gallery: JSON.parse \("(.*?);', re.S)
    result = re.search(image_pattern, html)
    if result:
        print(result.group(1))

def main():
    # html = get_page_detail('https://www.toutiao.com/a6602192672943768067/')
    # print(html)
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            parse_page_detail(html)
        # parse_page_detail(html)

if __name__ == '__main__':
    main()