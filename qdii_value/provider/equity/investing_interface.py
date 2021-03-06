from . import investing
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil import tz


tz_sh = tz.gettz('Asia/Shanghai')


def set_proxy(proxy):
    investing.proxies = {'https': 'http://' + proxy}


def search(kw, _type=None):
    res = investing.search(kw)
    if res is None:
        return None
    if _type:
        res = list(filter(lambda i: _type in i['search_main_subtext'], res))
    return [
        {
            'source_id': i['pair_ID'],
            'code': i['search_main_text'],
            'name': i['search_main_longtext'],
            'type': i['search_main_subtext']
        } for i in res
    ]


def sign_fix(s): 
    return s[1:] if s.startswith('+-') else s


def realtime(ids):
    global tz_sh
    if len(ids) == 0:
        return []
    res = investing.lists(ids)
    res_d = investing.lists_detail(ids)
    if res is None or res_d is None:
        return None
    ret = []
    for i in [{**p[0], **p[1]} for p in zip(res_d, res)]:
        c = {
            'source_id': i['pair_ID'],
            'source_name': i['pair_name'],
            'last': Decimal(i['last'].replace(',', '')),
            'change': Decimal(sign_fix(i['change_val'])),
            'change_percent': Decimal(sign_fix(i['change_percent_val'])),
            'volume': Decimal(i['volume'].replace(',', '')) if 'volume' in i.keys() else None,
            'is_open': i['exchange_is_open'],
            'time': datetime.fromtimestamp(int(i['last_timestamp']), tz=tz_sh)
        }
        if c['is_open'] is False and i['extended_hours_show_data'] != 'No':
            c['after_hour_price'] = Decimal(i['extended_price'])
            c['after_hour_percent'] = Decimal(i['extended_change_percent'][1:-2])
            c['after_hour_change'] = Decimal(i['extended_change'])
            c['after_hour_datetime'] = datetime.fromtimestamp(int(i['extended_shown_unixtime']))
        ret.append(c)
    return ret


def TO_FIX_2(f): 
    return Decimal(f).quantize(Decimal("0.00"))


def history(pair_id, limit=21):
    now = datetime.now(tz=tz_sh)
    start = now - timedelta(days=limit * 2)
    resp = [{
        'date': datetime.fromtimestamp(int(i[0])).strftime('%Y-%m-%d'),
        'open': TO_FIX_2(i[1]),
        'high': TO_FIX_2(i[2]),
        'low': TO_FIX_2(i[3]),
        'close': TO_FIX_2(i[4]),
        'volume': TO_FIX_2(i[5]) if not isinstance(i[5], str) or i[5].isnumeric() else None,
    } for i in investing.history(pair_id, int(start.timestamp()), int(now.timestamp()))]
    return resp[-limit:]
