import random
import requests
import demjson
from bs4 import BeautifulSoup

__url = 'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=50&year=&month=&rt=' + str(random.random())
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
    def get_tr(tr):
        td = tr.find_all('td')
        return {
            'sid': td[1].string,
            'name': td[2].string,
            'weight': td[6].string,
            'volume': td[7].string,
            'capital': td[8].string
        }
    return (n, list(map(get_tr, s.div.div.table.tbody.find_all('tr'))))
