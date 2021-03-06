from . import sina
import dateparser
from pytz import timezone

DATEPARSER_SETTINGS = {'TIMEZONE': 'Asia/Shanghai',
                       'RETURN_AS_TIMEZONE_AWARE': True}


def search(kw, _type=['11', '31', '33', '41']):
    return [
        {
            'source_id': i['code_full'],
            'code': i['code'].upper(),
            'name': i['name_cn'],
            'type': i['type']
        } for i in sina.search(kw, _type)
    ]


def realtime(ids):
    if len(ids) == 0:
        return []
    res = sina.realtime(*ids)
    ret = []
    for i in res:
        c = {
            'source_id': i['code_full'],
            'source_name': i['name'],
            'last': i['closing'],
            'change': i['delta'] if 'delta' in i.keys() else i['closing'] - i['last_closing'],
            'volume': i['volume'] if 'volume' in i.keys() else None,
        }
        if 'datetime' in i.keys():
            c['time'] = dateparser.parse(i['datetime']).astimezone(
                tz=timezone(DATEPARSER_SETTINGS['TIMEZONE']))
        else:
            c['time'] = dateparser.parse(
                i['date'] + ' ' + i['time'], settings=DATEPARSER_SETTINGS)
        if (c['last'] == 0):
            c['change'] = 0
            c['change_percent'] = 0
        elif 'percent' in i.keys():
            c['change_percent'] = i['percent']
        else:
            c['change_percent'] = c['change'] / i['last_closing'] * 100
        ago = dateparser.parse('5 minutes ago', settings=DATEPARSER_SETTINGS)
        c['time'] = c['time'].replace(year=ago.year)  # temp fix for new year
        c['is_open'] = c['time'] > dateparser.parse('5 minutes ago', settings=DATEPARSER_SETTINGS)
        if not c['is_open'] and 'after_hour_percent' in i.keys():
            c['after_hour_price'] = i['after_hour_price']
            c['after_hour_percent'] = i['after_hour_percent']
            c['after_hour_change'] = i['after_hour_delta']
            c['after_hour_datetime'] = dateparser.parse(i['after_hour_datetime'])
        ret.append(c)
    return ret


def history(*args, **kwargs):
    return [{
            'date': i['date'],
            'open': i['open'],
            'high': i['high'],
            'low': i['low'],
            'close': i['close'],
            'volume': i['volume'],
            } for i in sina.history(*args, **kwargs)]
