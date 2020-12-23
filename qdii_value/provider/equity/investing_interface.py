from . import investing
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil import tz


tz_sh = tz.gettz('Asia/Shanghai')


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
    global tz_sh
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
            'time': datetime.fromtimestamp(int(i['last_timestamp']), tz=tz_sh)
        } for i in res
    ]


TO_FIX_2 = lambda f: Decimal(f).quantize(Decimal("0.00"))


def history(pair_id, limit=21):
    now = datetime.now(tz=tz_sh)
    start = now - timedelta(days=limit * 2)
    resp = [{
        'date': datetime.fromtimestamp(int(i[0])).strftime('%Y-%m-%d'),
        'open': TO_FIX_2(i[1]),
        'high': TO_FIX_2(i[2]),
        'low' : TO_FIX_2(i[3]),
        'close': TO_FIX_2(i[4]),
        'volume': TO_FIX_2(i[5]),
    } for i in investing.history(pair_id, int(start.timestamp()), int(now.timestamp()))]
    return resp[-limit:]
