# Partial code from https://github.com/fasionchan/finance by Chen Yanfei


import requests
import datetime
from decimal import Decimal


def RET_N(a): return None


# search
SEARCH_URL = 'https://suggest3.sinajs.cn/suggest/type=%s&key=%s&name='

SEARCH_TYPES = {'11': "A 股", '12': "B 股", '13': "权证", '14': "期货", '15': "债券", '21': "开基",
                '22': "ETF", '23': "LOF", '24': "货基", '25': "QDII", '26': "封基", '31': "港股", '32': "窝轮",
                '33': "港指", '41': "美股", '42': "外期", '71': "外汇", '72': "基金", '73': "新三板", '74': "板块",
                '75': "板块", '76': "板块", '77': "板块", '78': "板块", '79': "板块", '80': "板块", '81': "债券",
                '82': "债券", '85': "期货", '86': "期货", '87': "期货", '88': "期货", '100': "指数", '101': "基金",
                '102': "指数", '103': "英股", '104': "国债", '105': "ETF", '106': "ETF", '107': "MSCI", '111': "A股",
                '120': "债券",
                }

SEARCH_FIELDS = ['corp', 'type', 'code', 'code_full']

SEARCH_TYPE_ID = {
    '11': lambda p: p['code_full'],
    '31': lambda p: 'hk' + p['code_full'],
    '41': lambda p: 'gb_'
}


def search(kw, types=[]):
    results = []
    raw = requests.get(SEARCH_URL % (','.join(types), kw)
                       ).text.split('"')[1].split(';')
    for line in raw:
        data = line.split(',')
        r = dict(zip(SEARCH_FIELDS, data))
        r['code_full'] = r['type'] + '#' + r['code_full']
        r['type'] = SEARCH_TYPES.get(r['type'])
        results.append(r)
    return results


# realtime
REALTIME_URL = 'http://hq.sinajs.cn/?list=%s'

CN_STATUS = {
    '00': None,
    '01': '临停1H',
    '02': '停牌',
    '03': '停牌',
    '04': '临停',
    '05': '停1/2',
    '07': '暂停',
    '-1': '无记录',
    '-2': '未上市',
    '-3': '退市'
}

REALTIME_FIELDS = {
    '11': [('corp', str), ('opening', Decimal), ('last_closing', Decimal),
           ('closing', Decimal), ('highest', Decimal), ('lowest', Decimal),
           ('buy', Decimal), ('sell', Decimal), ('volume', Decimal), ('deal', Decimal),
           ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N),
           ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N),
           ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N),
           ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N), ('', RET_N),
           ('date', str), ('time', str), ('status', CN_STATUS.get)
           ],
    '31': [('corp_en', str), ('corp', str), ('opening', Decimal),
           ('last_closing', Decimal), ('highest', Decimal), ('lowest', Decimal),
           ('closing', Decimal), ('delta', Decimal), ('percent', Decimal),
           ('buy', Decimal), ('sell', Decimal), ('volume', Decimal), ('deal', Decimal),
           ('pe', Decimal), ('yield_w', Decimal), ('52w_high', Decimal),
           ('52w_low', Decimal), ('date', str), ('time', str)
           ],
    '41': [('corp', str), ('closing', Decimal), ('percent', Decimal), ('time', str),
           ('delta', Decimal), ('opening', Decimal), ('highest', Decimal),
           ('lowest', Decimal), ('52w_highest', Decimal), ('52w_lowest', Decimal), 
           ('volume', Decimal), ('avg_vol', Decimal), ('total_share', Decimal), 
           ('eps', str), ('pe', str), ('', RET_N), ('beta', Decimal), 
           ('dividend', str), ('income', str), ('shares', Decimal), ('', RET_N),
           ('after_hour_price', Decimal), ('after_hour_percent', Decimal),
           ('after_hour_delta', Decimal), ('after_hour_datetime', str), ('datetime', str),
           ('last_closing', Decimal), ('after_hour_volume', Decimal)
           ]
}


def realtime_api(*l):
    raw = requests.get(REALTIME_URL % (','.join(l),)).text
    return [line.split('"')[1].split(',')
            for line in raw.split('\n') if line]


def parse_symbol_11(symbol): return symbol
def parse_symbol_31(symbol): return 'rt_hk%s' % (symbol.upper())
def parse_symbol_41(symbol): return 'gb_%s' % (symbol.lower())


def parse_symbol(symbol):
    typ, code = symbol.split('#')
    symbol = globals()[f'parse_symbol_{typ}'](code)
    return symbol, REALTIME_FIELDS[typ]


def realtime(*symbols):
    results = []
    f_symbols_pair = [parse_symbol(symbol) for symbol in symbols]
    f_symbols = [p[0] for p in f_symbols_pair]
    fmts = [p[1] for p in f_symbols_pair]
    data = realtime_api(*f_symbols)
    for symbol in zip(symbols, data, fmts):
        pairs = zip(symbol[2], symbol[1])
        kvs = [(key, cls(value)) for (key, cls), value in pairs]
        kvs.append(('code_full', symbol[0]))
        results.append(dict(kvs))
    return results


def test():
    print(search('腾讯'))
    print(search('平安'))
    print(search('msft'))
    print(search('00909'))

    print(realtime('31#00358', '11#sz000002', '41#bili'))


if __name__ == '__main__':
    test()
