import requests
from bs4 import BeautifulSoup
from functools import partial

__url = 'https://funds.dbs.com.cn/DBS/zh-CN/FundDetail/Overview?id={}&currencyId=CU$$$$${}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def get_tr(keys, trs):
    if len(keys) > len(trs):
        return None
    tds = trs.find_all('td')
    vals = list(map(lambda td: td.text.strip(), tds))[:len(keys)]
    return dict(zip(keys, vals))


def lists(fund_id):
    fid = fund_id.split('#')
    code = fid[0]
    currency = fid[1] if len(fid) > 1 else 'CNH'
    
    r = requests.get(__url.format(str(code), currency), headers=headers)
    s = BeautifulSoup(r.content, features='lxml')
    n = s.find(id='snapshotTitleDiv').text.strip()
    if len(n) == 0:
        return None
    d = s.find(id='portfolioHeading').find(class_='titleBarNote').text
    p = s.find(id='portfolioTopHoldingsDataDiv')
    if p is None:
        return None
    assets_keys = ['type', 'long', 'short', 'percent']
    a = s.find(id='portfolioAssetAllocationLongAndShortEqutity')
    assets = list(map(partial(get_tr, assets_keys), a.table.find_all('tr')))[1:]
    stock = list(filter(lambda a: a['type'] == '股票', assets))

    equities_keys = ['name', 'industry', 'location', 'weight']
    equities = filter(lambda e: e is not None, map(partial(get_tr, equities_keys), p.table.find_all('tr')))
    return {
        "fund_name": n, 
        "last_update": d, 
        "equities": list(equities)[1:],
        "equities_percent": stock[0]['percent'] if len(stock) > 0 else None
    }
