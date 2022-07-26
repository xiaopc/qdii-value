from . import msn
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil import tz


tz_sh = tz.gettz('Asia/Shanghai')
TYPE_MAP = {'ST': '股票', 'FO': '基金', 'FE': 'ETF', 'XI': '指数'}


def parse_utc_str(str):
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S"
    return (datetime.strptime(str.split('.')[0], UTC_FORMAT) + timedelta(hours=8)).replace(tzinfo=tz_sh)


def search(kw, _type=None):
    res = msn.search(kw)
    if res is None or len(res) == 0:
        return None
    return [
        {
            'source_id': i['SecId'],
            'code': i['FullInstrument'].split('.')[2] if len(i['FullInstrument'].split('.')) > 2 else i['FullInstrument'],
            'name': i['OS0LN'],
            'type': TYPE_MAP['FO'] if i['OS010'] == 'FO' else '{} - {}'.format(TYPE_MAP[i['OS010']], i['AC040'])
        } for i in res
    ]


def realtime(ids):
    global tz_sh
    if len(ids) == 0:
        return []
    res = msn.lists(ids)
    if res is None or len(res) == 0:
        return None
    return [{
        'source_id': i[0]['instrumentId'],
        'source_name': i[0]['localizedAttributes']['zh-cn']['displayName'] if 'zh-cn' in i[0]['localizedAttributes'].keys() else i[0]['displayName'],
        'last': i[0]['price'],
        'change': i[0]['priceChange'],
        'change_percent': i[0]['priceChangePercent'],
        'volume': i[0]['accumulatedVolume'] if 'accumulatedVolume' in i[0].keys() else None,
        'is_open': (parse_utc_str(i[0]['timeLastUpdated']) + timedelta(minutes=5)) > datetime.now(tz_sh),
        'time': parse_utc_str(i[0]['timeLastTraded'])
    } for i in res]
