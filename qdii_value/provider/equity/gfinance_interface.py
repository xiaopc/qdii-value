from . import gfinance
from decimal import Decimal
from datetime import datetime
from dateutil import tz


tz_sh = tz.gettz('Asia/Shanghai')


def set_proxy(proxy):
    gfinance.proxies = {'https': 'http://' + proxy}


def search(kw, _type=None):
    res = gfinance.search(kw)
    return [
        {
            'source_id': i['full_ticker'],
            'code': i['code'],
            'name': i['name'],
            'type': i['market']
        } for i in res
    ]


def realtime(ids):
    global tz_sh
    if len(ids) == 0:
        return []
    res = gfinance.lists_detail(ids)
    ret = []
    for i in res:
        c = {
            'source_id': i['full_ticker'],
            'source_name': i['name'],
            'last': Decimal(i['trading']['last']),
            'change': Decimal(i['trading']['change']),
            'change_percent': Decimal(i['trading']['change_percent']),
            'time': datetime.fromtimestamp(i['last_timestamp'], tz=tz_sh),
        }
        now = datetime.now(tz=tz_sh)
        c['is_open'] = now < i['end_trading_dt'] and now > i['start_trading_dt']
        if c['is_open'] is False and i['extended_trading'] is not None:
            c['after_hour_price'] = Decimal(i['extended_trading']['last'])
            c['after_hour_percent'] = Decimal(i['extended_trading']['change_percent'])
            c['after_hour_change'] = Decimal(i['extended_trading']['change'])
            c['after_hour_datetime'] = datetime.fromtimestamp(i['extended_timestamp'], tz=tz_sh)
        ret.append(c)
    return ret


def history(_id, limit=21):
    resp = [{
        'date': i['datetime'].strftime('%Y-%m-%d'),
        'close': i['trading']['last'],
        'change': i['trading']['change'],
        'change_percent': i['trading']['change_percent'],
        'volume': i[volume],
    } for i in gfinance.history(_id, 3)]
    return resp[-limit:]
