import requests
from urllib.parse import quote
import time

__base_path = 'https://tw.stock.yahoo.com/_td-stock/api/resource/{}'
__session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
proxies = None
timeout = 10.


def __get(url, get_data=True):
    rsp = __session.get(__base_path.format(url), headers=headers, proxies=proxies, timeout=timeout)
    if rsp.status_code != 200:
        raise Exception('网络错误: ' + rsp.status_code)
    return rsp.json()


# {"ResultSet":{"Query":"se","Result":[{"symbol":"SE","name":"Sea Limited","exch":"NYQ","type":"S","exchDisp":"NYSE","typeDisp":"權益"}, ...]}}
def search(kw):
    url = 'WaferAutocompleteService;view=json&query={}'.format(quote(kw))
    return __get(url)['ResultSet']['Result']


# [{"ask":"616","bid":"615","change":"0","changePercent":"+0.00%","changeStatus":"equal","exchange":"TAI","holdingType":"EQUITY","limitDown":false,"limitDownPrice":"554","limitUp":false,"limitUpPrice":"676","marketStatus":"open","messageBoardId":"finmb_380075_lang_zh","previousVolume":"15169000","price":"615","regularMarketDayHigh":"618","regularMarketDayLow":"612","regularMarketOpen":"618","regularMarketPreviousClose":"615","regularMarketTime":"2021-09-14T04:15:53Z","relatedSymbol":null,"relatedSymbolName":null,"sectorId":"40","sectorName":"半導體","symbol":"2330.TW","symbolName":"台積電","systexId":"2330","turnoverM":"5984.153","volume":"9730000","previousVolumeK":15169,"volumeK":9730}, ...]
def lists(symbols):
    url = 'StockServices.stockList;symbols={}&ecma=default&intl=tw&lang=zh-Hant-TW&region=TW&site=finance&tz=Asia%2FChongqing&ver=1.2.1139'.format('%2C'.join(symbols))
    return __get(url)
