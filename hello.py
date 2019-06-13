#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from abstest import my_abs, move
print("hello world\n", "你是谁\n", "who are you")

print("hello world\n", "你是谁\n", "who are you")
age = 20
if age >= 18:
    print("adult")
elif age > 6:
    print("teenager")
else:
    print("kid")


# 定义函数
# def my_abs(x):
#     if x > 0:
#         return x
#     else:
#         return -x

print(my_abs(-99))
print(move(100, 100, 60, math.pi / 6))

from urllib import request
# with request.urlopen('http://www.douban.com/') as f:
#     data = f.read()
#     print('Status:', f.status, f.reason)
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print('Data:', data.decode('utf-8'))

# req = request.Request('http://www.douban.com/')
# req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# with request.urlopen(req) as h:
#     print('Status:', h.status, h.reason)
#     for a, b in h.getheaders():
#         print('%s: %s' % (a, b))
#     print('Data:', h.read().decode('utf-8'))

import socket
import socks
import requests

# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
# socket.socket = socks.socksocket
proxies = {
    'http':'socks5://127.0.0.1:1086',
    'https': 'socks5://127.0.0.1:1086'
}
headerss = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
url = 'https://www.pornhub.com/'
htm = requests.get(url,headers=headerss, proxies=proxies)
print(htm.text)

def generatorText():
    for i in range(10):
        print(i)
        yield
        print('第 %d 次',i)


o = generatorText()

