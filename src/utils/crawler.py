# coding:utf-8
'''
Here are some utilities which can help us search something from Baidu or Google.
'''
import requests
from bs4 import BeautifulSoup
import json
from scrapy.selector import Selector
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


def getHTMLText(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception:
        return ''


def baidu_parse(html):
    ulist = []
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', {'class': 'result c-container'})
    if not items:
        items = soup.find_all('div', {'class': 'result c-container '})
    for node in items:
        try:
            abstract_node = node.find('div', {'class': 'c-abstract c-abstract-en'})
            if not abstract_node:
                abstract_node = node.find('div', {'class': 'c-abstract'})
            ctools = node.find('div', {'class': 'c-tools'})
            abstract = abstract_node.text
            title = json.loads(ctools['data-tools'].replace('\\', ''))['title']
            ulist.append({
                'title': title,
                'content': abstract
            })
        except Exception as ex:
            print(str(ex))
    return ulist


def google_parse(html):
    page = Selector(text=html)
    rs = []
    for ans in page.css('div.g'):
        title = ''.join(ans.css('h3').css('*::text').extract())
        content = ''.join(ans.css('span.st').css('*::text').extract())
        url = ans.css('*.r a::attr(href)').extract()
        try:
            url = re.findall('(http.*)', url[0])
            url = re.sub('&.*', '', url[0])
            rs.append({
                'url': url,
                'content': content,
                'title': title,
            })
        except Exception:
            pass
    return rs


# url = 'https://www.baidu.com/s?wd=jie%20tang&usm=1&tn=baidu&f=13&ie=utf-8&nojc=1&rqlang=en'
# html = getHTMLText(url)
# print(baidu_parse(html))