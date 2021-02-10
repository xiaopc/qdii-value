if __package__:
    from .provider.equity import *
else:
    from provider.equity import *
from datetime import datetime, timedelta
from dateutil import tz
from itertools import chain, groupby
from decimal import Decimal

# 以每日此时间前收盘作为交易日分界
TRADING_START_HOUR = 8

tz_sh = tz.gettz('Asia/Shanghai')
now = datetime.now(tz=tz_sh)
zero_today = now - timedelta(hours=now.hour, minutes=now.minute,
                             seconds=now.second, microseconds=now.microsecond)
TRADE_TODAY = zero_today + timedelta(hours=TRADING_START_HOUR)


def divide_by_provider(equities):
    d = dict([(p['id'], (p, [])) for p in EQUITY_PROVIDER])
    for e in equities:
        d[e['source']][1].append(e)
    return d


def get_data_from_provider(provider, equities):
    source_ids = [e['source_id'] for e in equities]
    res = provider['object'].realtime(source_ids)
    for item in equities:
        item_res = filter(lambda r: r['source_id'] == item['source_id'], res)
        try:
            status = next(item_res)
            item.update(status)
        except StopIteration:
            continue
    return equities


def get_history_from_provider(provider, equities, **kwargs):
    items = []
    for e in equities:
        r = e.copy()
        r['history'] = provider['object'].history(e['source_id'], **kwargs)
        items.append(r)
    return items


def combine_summary(d):
    equities = list(chain(*d.values()))
    for e in equities:
        e['weight'] = Decimal(e['weight'])
        e['is_today'] = e['time'] > TRADE_TODAY
    equities.sort(key=lambda e: e['weight'], reverse=True)

    total_w = sum([e['weight'] for e in equities])
    today_equities = list(filter(lambda e: e['is_today'], equities))
    if len(today_equities) > 0:
        today_w = Decimal(sum([e['weight'] for e in today_equities]))
        today_p = Decimal(sum([e['weight'] * e['change_percent'] / 100 for e in today_equities]))
        total_p = today_p / (total_w / 100)
        today_p /= today_w / 100
    else:
        total_p = Decimal(sum([e['weight'] * e['change_percent'] / 100 for e in equities]))
        total_p /= total_w / 100
        today_w, today_p = Decimal(0), Decimal(0)
    latest = max([e['time'] for e in equities])

    return equities, {
        'last_update': latest,
        'total_weight': total_w,
        'total_percent': total_p,
        'today_weight': today_w,
        'today_percent': today_p
    }


def single_fetch(equity):
    d = dict([(p['id'], p) for p in EQUITY_PROVIDER])
    return get_data_from_provider(d[equity['source']], [equity])[0]

def fetch(equities):
    d = divide_by_provider(equities)
    for provider in d:
        d[provider] = get_data_from_provider(*d[provider])
    return combine_summary(d)

def fetch_history(equities, **kwargs):
    d = divide_by_provider(equities)
    s = []
    for provider in d:
        s += get_history_from_provider(*d[provider], **kwargs)
    return s
