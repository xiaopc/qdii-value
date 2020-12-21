import requests
from bs4 import BeautifulSoup
import re

__url = 'https://www.bloomberg.com/quote/{}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-HK;q=0.8,zh-TW;q=0.7,en-US;q=0.6,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
}

proxies = None


def lists(fund_id):
    r = requests.get(__url.format(fund_id), headers=headers, proxies=proxies, allow_redirects=False)
    if r.status_code == 404:
        return None
    elif len(r.content) == 0:
        raise Exception('请求 Bloomberg 时遇到反爬.')
    s = BeautifulSoup(r.content, features='lxml')
    n = s.find(class_=re.compile('companyName')).string
    p = s.find_all(class_=re.compile('table_'))
    p = list(filter(lambda t: t.h2.span.string == 'Fund Top Holdings', p))
    if len(p) == 0:
        return None

    def get_tr(tr):
        td = tr.find_all(class_=re.compile('cell_'))
        return {
            'code': td[0].a.span.string,
            'name': td[0].a.div.string,
            'volume': td[1].string,
            'capital': td[2].string,
            'weight': td[3].string[:-1]
        }
    return {"fund_name": n, "last_update": None, "equities": list(map(get_tr, p[0].find_all(class_=re.compile('row'))))}
