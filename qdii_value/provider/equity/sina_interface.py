from . import sina
import dateparser
from datetime import datetime, timedelta


def search(kw, _type=['11', '31', '41']):
    res = sina.search(kw, _type)
    return [
        {
            'source_id': i['code_full'],
            'code': i['code'].upper(),
            'name': i['corp'],
            'type': i['type']
        } for i in res
    ]


def realtime(ids):
    if len(ids) == 0:
        return []
    res = sina.realtime(*ids)
    ret = [
        {
            'source_id': i['code_full'],
            'name': i['corp'],
            'last': i['closing'],
            'change': i['delta'] if 'delta' in i.keys() else i['closing'] - i['last_closing'],
            'change_percent': i['percent'] if 'percent' in i.keys() else (i['closing'] - i['last_closing']) / i['last_closing'] * 100,
            'time': dateparser.parse(i['datetime']) if 'datetime' in i.keys() else dateparser.parse(i['date'] + ' ' + i['time'], settings={'TIMEZONE': 'Asia/Shanghai', 'RETURN_AS_TIMEZONE_AWARE': True})
        } for i in res
    ]
    for i in ret:
        i['is_open'] = i['time'] > dateparser.parse('5 minutes ago', settings={'TIMEZONE': 'Asia/Shanghai', 'RETURN_AS_TIMEZONE_AWARE': True})
    return ret
