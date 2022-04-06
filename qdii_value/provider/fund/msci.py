import requests
import xlrd
import dateparser
import re


__url_xls = 'https://app2.msci.com/eqb/custom_indexes/{}_performance.xls'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def get_row_item(col_name, row, header):
    return row[header.index(col_name)]


def lists(fund_id):
    r = requests.get(__url_xls.format(str(fund_id.lower())), headers=headers)
    if r.status_code != 200:
        raise Exception('HTTP {}, 请确认 https://app2.msci.com/eqb/custom_indexes/{}_performance.html'.format(r.status_code, fund_id))
    book = xlrd.open_workbook(file_contents=r.content)
    sheet = book.sheet_by_index(0)
    r = {
        'fund_name': sheet.cell_value(0, 0),
        'last_update': None,
        'equities': []
    }
    cur_row, is_in, cols = 1, False, []
    while True:
        line = sheet.row_values(cur_row)
        if 'Constituents' in line[0]:
            r['last_update'] = dateparser.parse(line[0].split('for ')[1].strip()).strftime('%Y-%m-%d')
        elif 'MSCI Code' in line[0]:
            cols = line
            is_in = True
        elif is_in and len(line[0]) < 1:
            break
        elif is_in:
            r['equities'].append({
                'code': get_row_item('Reuters Code (RIC)', line, cols),
                'name': get_row_item('Security Name', line, cols),
                'weight': get_row_item('Weight%', line, cols),
            })
        cur_row += 1
    return r
