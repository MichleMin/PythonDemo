from  bs4 import BeautifulSoup
from  pyquery import PyQuery as pq

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc, 'lxml')
# print(soup.prettify())
# print(soup.title)
# print(type(soup.title))
# print(soup.head)
# print(type(soup.p))
# print(soup.find(id='link3'))
# for i,child in enumerate(soup.p.children):
#     print(i,child)
# for link in soup.find_all('a'):
#     print(link.get('href'))
# print(soup.get_text())
# print(soup.select('a'))
# for link in soup.select('p  #link1'):
#     print(link.get_text())

doc = pq(html_doc)
print(doc('.story').text())
for item in doc('a').items():
    # print(item)
    print(item.attr('href'))
    print(item.text())

from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.open()')
browser.switch_to.window(browser.window_handles[1])
browser.get('https://www.baidu.com')
print(browser.get_cookies())
# input = browser.find_element_by_id('key')
# input.send_keys('iPhone')
# button = browser.find_element_by_class_name('button')#browser.find_element_by_css_selector('#search > div > div.form > button')
# button.click()
# print(button.text)