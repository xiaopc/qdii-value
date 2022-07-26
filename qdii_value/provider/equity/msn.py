import requests
from decimal import Decimal


__assets_base_path = 'https://assets.msn.com/service/Finance/{}?apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&ocid=finance-finance-Peregrine&market=zh-cn&fdhead={}&ids={}&wrapodata=false'
__fhead = ['prg-1sxfother1', 'prg-1sw-fidbrefc', 'prg-1sw-fiplog', 'prg-1sw-clctrl', '1s-winauthservice', 'prg-1sw-colcons-rev', 'prg-1sw-bdgt1', '1s-fk-bdg', '1s-p2-brknb', 'prg-1sbgbanner', 'prg-1sfakebg', 'prg-1sw-wxbdg2', 'prg-1sw-clrot', 'prg-1s-mtsn', 'prg-1sw-wxrus', '1s-fcrypt', 'prg-1sw-firowlcombc', 'prg-1sw-firoc', 'prg-1sw-hdukr', 'prg-1sw-sbn-mm', 'prg-1sw-pmosg', 'prg-1sw-list', '1s-rpssecautht', 'prg-1sw-p1wtrclm', 'prg-1sw-mbnodp', 'prg-1sw-aqlmtrt', 'prg-1sw-wxcfwf', 'prg-1sw-pllmtrt', 'prg-1sw-stml2', 'prg-1sw-ani1', 'prg-1sw-tsc']
__session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Origin': 'https://www.msn.com',
    'Referer': 'https://www.msn.com/'
}
timeout = 10.


def __get(action, ids):
    rsp = __session.get(__assets_base_path.format(action, ','.join(__fhead), ','.join(ids)), headers=headers, timeout=timeout)
    if rsp.status_code > 300:
        raise Exception('网络错误: {}'.format(rsp.status_code))
    return rsp.json(parse_float=Decimal)


def search(kw):
    rsp = __session.get('https://finance-services.msn.com/Market.svc/MTAutocomplete?count=250&q={}&locale=zh-cn'.format(kw), headers=headers, timeout=timeout)
    if rsp.status_code != 200:
        raise Exception('网络错误: {}'.format(rsp.status_code))
    return rsp.json()['data']


def lists(symbols):
    return __get('Quotes', symbols)

