from . import yahootw
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil import tz


tz_sh = tz.gettz('Asia/Shanghai')
UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def set_proxy(proxy):
    yahootw.proxies = {'https': 'http://' + proxy}


def search(kw, _type=None):
    res = yahootw.search(kw)
    if res is None or len(res) == 0:
        return None
    return [
        {
            'source_id': i['symbol'],
            'code': i['symbol'].split('.')[0],
            'name': i['name'],
            'type': '{} - {}'.format(i['typeDisp'], i['exchDisp'])
        } for i in res
    ]


def realtime(ids):
    global tz_sh
    if len(ids) == 0:
        return []
    res = yahootw.lists(ids)
    if res is None or len(res) == 0:
        return None
    return [{
        'source_id': i['symbol'],
        'source_name': i['symbolName'],
        'last': Decimal(i['price']) if i['price'] != '-' else Decimal(0),
        'change': Decimal(i['change']) if i['price'] != '-' else Decimal(0),
        'change_percent': Decimal(i['changePercent'][:-1]) if i['price'] != '-' else Decimal(0),
        'volume': Decimal(i['volume']) if 'volume' in i.keys() else None,
        'is_open': i['marketStatus'] == 'open',
        'time': (datetime.strptime(i['regularMarketTime'], UTC_FORMAT) + timedelta(hours=8)).replace(tzinfo=tz_sh)
    } for i in res]
