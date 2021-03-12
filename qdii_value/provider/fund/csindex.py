import requests
import xlrd
from datetime import datetime
from bs4 import BeautifulSoup
import re

__url = 'http://www.csindex.com.cn/zh-CN/indices/index-detail/{}'
__url_xls = 'http://www.csindex.com.cn/uploads/file/autofile/closeweight/{}closeweight.xls'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def lists(fund_id):
    r = requests.get(__url_xls.format(str(fund_id)), headers=headers)
    if r.status_code == 200:
        book = xlrd.open_workbook(file_contents=r.content)
        sheet = book.sheet_by_index(0)
        r = {
            "fund_name": sheet.cell_value(1, 2),
            "last_update": datetime(*xlrd.xldate_as_tuple(sheet.cell_value(1, 0), book.datemode)).strftime('%Y-%m-%d'),
            "equities": []
        }
        for i in range(1, sheet.nrows):
            line = sheet.row_values(i)
            r["equities"].append({
                'code': line[4],
                'name': line[5],
                'weight': line[8]
            })
        return r

    # else fetch 10
    r = requests.get(__url.format(str(fund_id)), headers=headers)
    if r.status_code != 200:
        return None
    s = BeautifulSoup(r.content, features='lxml')
    n = s.find('h1')
    if not n:
        return None
    d = s.find('h2', text='十大权重股')
    if not d:
        return None
    # d = re.search(r"\d{4}-\d{2}-\d{2}", d).group()
    p = list(filter(lambda node: node.name == 'table', d.next_siblings))[0]

    def get_tr(tr):
        td = tr.find_all('td')
        return {
            'code': td[0].string,
            'name': td[1].string,
            'weight': td[3].string
        }
    return {"fund_name": n.text, "last_update": d.next_sibling.text.split(':')[1], "equities": list(map(get_tr, p.tbody.find_all('tr')))}
