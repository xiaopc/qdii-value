import requests
from urllib.parse import quote
import time

__base_path = 'https://cnappapi.investing.com/{}&lang_ID=6&time_utc_offset=28800'
__session = requests.Session()
headers = {
    'User-Agent': 'Investing.China/0.0.1 CFNetwork/1128.0.1 Darwin/19.6.0',
    'ccode': 'CN',
    'x-meta-ver': '14',
    'x-os': 'ios',
    'ccode_time': '{:.4f}'.format(time.time()),
}
proxies = None
timeout = 20.

def __get(url):
    rsp = __session.get(__base_path.format(url), headers=headers, proxies=proxies, timeout=timeout).json()
    if rsp['error']['display_message'] is not "":
        raise Exception(rsp['error']['display_message'])
    return rsp['data']

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
