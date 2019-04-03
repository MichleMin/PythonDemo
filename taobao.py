from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import  PyQuery as pq
import re

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)

def search():
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))
        )
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist > div > div .items .item'))
        )
        html = browser.page_source
        doc = pq(html)
        # print(doc)
        items = doc('#mainsrp-itemlist > div > div .items .item').items()
        for item in items:
            # imageHtml = item.find('.p-img')
            # imagePattern = re.compile('<div xmlns.*?src=(.*?)/>', re.S)
            # image = re.search(imagePattern, str(imageHtml).strip())
            # print(image)
            # priceHtml = item.find('.p-price')
            # pricePattern = re.compile('div.*?<i>(.*?)</i>', re.S)
            # price = re.search(pricePattern, str(priceHtml))
            product = {
                'image': item.find('.pic .img').attr('src'),
                'price': item.find('.price').text(),
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text()
            }
            print(product)

    except TimeoutException:
        return None


def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, total+1):
        next_page(i)

if __name__ == '__main__':
    main()
