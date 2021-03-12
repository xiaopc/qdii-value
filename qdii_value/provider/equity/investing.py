import requests
from urllib.parse import quote
import time

__base_path = 'https://cnappapi.investing.com/{}&lang_ID=6&time_utc_offset=28800'
__session = requests.Session()
headers = {
    'User-Agent': 'Investing.China/0.0.1 CFNetwork/1128.0.1 Darwin/19.6.0',
    'ccode': 'CN',
    'x-app-ver': '144',
    'x-meta-ver': '14',
    'x-os': 'ios',
    'ccode_time': '{:.4f}'.format(time.time()),
}
proxies = None
timeout = 10.


def __get(url, get_data=True):
    rsp = __session.get(__base_path.format(url), headers=headers, proxies=proxies, timeout=timeout)
    if rsp.status_code != 200:
        raise Exception('网络错误: ' + rsp.status_code)
    rsp = rsp.json()
    if 'error' in rsp.keys() and rsp['error']['display_message'] != "":
        raise Exception(rsp['error']['display_message'])
    return rsp['data'] if get_data else rsp


# [{'pair_ID': 9235, 'search_main_text': 'RS', 'search_main_longtext': 'Reliance Steel & Aluminum Co.', 'exchange_flag_ci': 5, 'search_main_subtext': '股票 - 纽约'}, ...]
def search(kw):
    url = 'search.php?string={}'.format(quote(kw))
    return __get(url)['pairs_attr']


# {'overview_table': [{'key': ..., 'val': ...},], 'info_header': {...}, 'technical_summary': [...], ...}
def detail(pair_id):
    url = 'get_screen.php?v2=1&skinID=1&include_pair_attr=false&screen_ID=22&pair_ID=' + str(pair_id)
    return __get(url)[0]['screen_data']['pairs_data'][0]


# [{'pair_ID': 8874, 'last': '11,115.00', 'change_percent_val': '-1.24', 'change_precent': '(-1.24%)', 'change_val': '-140.00', 'change': '-140.00', 'pair_change_color': '#0d9d00', 'localized_last_step_arrow': 'down_green', 'exchange_is_open': True, 'last_timestamp': '1600318417', 'is_cfd': True, 'earning_alert': 'no', 'exchange_name': '', 'pair_name': '纳斯达克100', 'pair_table_row_main_subtext': '期货', 'pair_innerpage_quote_subtext': '实时差价合约', 'currency_in': 'USD', 'pair_type_section': 'futureCash', 'pair_name_base': 'USTEC', 'exchange_country_ID': 0, 'zmqIsOpen': 'isOpenPair-8874:'}, ]
def lists(pair_ids):
    url = 'get_screen.php?v2=1&skinID=1&include_pair_attr=false&screen_ID=30&pairs_IDs=' + ','.join(map(lambda x: str(x), pair_ids))
    return __get(url)[0]['screen_data']['pairs_additional']


# [{'pair_ID': 23647, 'last': '71.71', 'change_percent_val': 3.18, 'change_val': 2.21, 'change': '+2.21', 'change_precent': '(+3.18%)', 'change_precent_raw': '+3.18', 'extended_price': '70.94', 'extended_change': '-0.77', 'extended_change_percent': '(-1.07%)', 'extended_shown_datetime': '6:08:41', 'extended_shown_unixtime': '1609970921', 'extended_hours_show_data': 'After', 'pair_change_color': '#FF0000', 'extended_change_color': '#0d9d00', 'technical_summary_color': '#0d9d00', 'technical_summary_text': '强力买入', 'localized_last_step_arrow': 'up_red', 'extended_localized_last_step_arrow': 'down_green', 'exchange_is_open': False, 'last_timestamp': 1609966799, 'last_close_value': '71.71', 'open': '71.40', 'bond_coupon': '', 'day_range': '70.90 - 72.41', 'low': '70.9', 'high': '72.41', 'a52_week_range': '29.78 - 72.41', 'a52_week_low': '29.78', 'a52_week_high': '72.41', 'bond_price_range': '-', 'bond_price': '', 'isCrypto': False, 'turnover_volume': '4,844,401', 'avg_volume': '2,114,164', 'volume': '4,844,401', 'formatted_volume': '4,844,401 (2,114,164)'}, }
def lists_detail(pair_ids):
    url = 'get_screen.php?skinID=1&screen_ID=30&pairs_IDs=' + ','.join(map(lambda x: str(x), pair_ids))
    return __get(url)[0]['screen_data']['pairs_additional']


# 21 days most (including this exchange day)
# [{'start_timestamp': 1608588000000, 'open': 1774.43, 'max': 1777.32, 'min': 1764.84, 'close': 1773.84, 'navigation': 'd'}, ...]
def history_o(pair_id, limit=21):
    url = 'chart_range.php?range=6m&skinID=1&pair_ID=' + str(pair_id)
    return __get(url, False)['candles'][-limit:]


def history(pair_id, start_timestamp, end_timestamp):
    now_ts = int(time.time())
    url = 'http://tvc3.investingapp.net/7d263b5e085ea9ddbd3d7274bdec1c82/{}/6/8/history?symbol={}&resolution=D&from={}&to={}'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko)',
        'Origin': 'http://tvc-invdn-com.akamaized.net',
        'Referer': 'http://tvc-invdn-com.akamaized.net/ios/1.12.8/0/index1-prod.html'
    }
    resp = requests.get(url.format(now_ts, pair_id, start_timestamp, end_timestamp), headers=header, proxies=proxies, timeout=timeout).json()
    if 't' in resp.keys():
        return zip(resp['t'], resp['o'], resp['h'], resp['l'], resp['c'], resp['v'])
    else:
        return None
