from . import investing
from decimal import Decimal
from datetime import datetime
from dateutil import tz


def set_proxy(proxy):
    investing.proxies = {'https': 'http://' + proxy}


def search(kw, _type=None):
    res = investing.search(kw)
    if _type:
        res = list(filter(lambda i: _type in i['search_main_subtext'], res))
    return None if res is None else [
        {
            'source_id': i['pair_ID'],
            'code': i['search_main_text'],
            'name': i['search_main_longtext'],
            'type': i['search_main_subtext']
        } for i in res
    ]


def realtime(ids):
    if len(ids) == 0:
        return []
    res = investing.lists(ids)
    return None if res is None else [
        {
            'source_id': i['pair_ID'],
            'name': i['pair_name'],
            'last': Decimal(i['last'].replace(',', '')),
            'change': Decimal(i['change_val']),
            'change_percent': Decimal(i['change_percent_val']),
            'is_open': i['exchange_is_open'],
            'time': datetime.fromtimestamp(int(i['last_timestamp']), tz=tz.gettz('Asia/Shanghai'))
        } for i in res
    ]
