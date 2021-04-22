import random
import requests
import demjson
from bs4 import BeautifulSoup

__url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=50&year=&month=&rt=' + \
    str(random.random())
__url_zcpz = 'http://fundf10.eastmoney.com/zcpz_{}.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def lists(fund_id):
    r = requests.get(__url.format(str(fund_id)), headers=headers)
    j = demjson.decode(r.content.decode('utf8').split('=', 1)[1][:-1])
    if j['content'] == "":
        return None
    s = BeautifulSoup(j['content'], features='lxml')
    n = s.div.div.h4.label.a.string
    d = s.div.div.h4.find('font').string

    r1 = requests.get(__url_zcpz.format(str(fund_id)), headers=headers)
    s1 = BeautifulSoup(r1.content.decode('utf8'), features='lxml')
    l1 = s1.find(class_='tzxq').tbody.tr.find_all('td')
    get_item = lambda i: float(0 if '-' in l1[i].string else l1[i].string[:-1])
    stock, dr = get_item(1), get_item(4)
    bond, cash = get_item(2), get_item(3)
    if stock + dr > 50:
        percents = stock + dr
    else:
        percents = 100 - bond - cash

    def get_tr(tr):
        td = tr.find_all('td')
        return {
            'code': td[1].string,
            'name': td[2].string,
            'weight': td[6].string[:-1],
            'volume': td[7].string,
            'capital': td[8].string
        }
    return {
        "fund_name": n,
        "last_update": d,
        "equities": list(map(get_tr, s.div.div.table.tbody.find_all('tr'))),
        "equities_percent": str(round(percents, 2))
    }
