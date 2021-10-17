import requests
import xlrd
from datetime import datetime
import re

__url_basic = 'https://www.csindex.com.cn/csindex-home/indexInfo/index-basic-info/{}'
__url_top = 'https://www.csindex.com.cn/csindex-home/index/weight/top10/{}'
__url_xls = 'https://csi-web-dev.oss-cn-shanghai-finance-1-pub.aliyuncs.com/static/html/csindex/public/uploads/file/autofile/closeweight/{}closeweight.xls'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def get_json(url):
    rsp = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    rsp = rsp.json()
    if rsp['code'] != '200':
        return None
    return rsp['data']


def lists(fund_id):
    r = requests.get(__url_xls.format(str(fund_id)), headers=headers)
    if r.status_code == 200:
        book = xlrd.open_workbook(file_contents=r.content)
        sheet = book.sheet_by_index(0)
        r = {
            'fund_name': sheet.cell_value(1, 2),
            'last_update': datetime.strptime(sheet.cell_value(1, 0), '%Y%m%d').strftime('%Y-%m-%d'),
            'equities': []
        }
        for i in range(1, sheet.nrows):
            line = sheet.row_values(i)
            is_duplicate = filter(lambda l: l['code'] == line[4], r['equities'])
            if len(list(is_duplicate)) > 0:
                continue
            r['equities'].append({
                'code': line[4],
                'name': line[5],
                'weight': line[9]
            })
        return r

    # else fetch 10
    r = get_json(__url_basic.format(str(fund_id)))
    if r is None:
        return None
    fund_name = r['indexFullNameCn']
    r = get_json(__url_top.format(str(fund_id)))
    if r is None:
        return None

    def get_tr(row):
        return {
            'code': row['securityCode'],
            'name': row['securityName'],
            'weight': row['weight']
        }
    return {'fund_name': fund_name, 'last_update': r['updateDate'], 'equities': list(map(get_tr, r['weightList']))}
