from . import eastmoney, hsbc, csindex, bloomberg

FUND_PROVIDER = [
    {
        'id': 'eastmoney',
        'name': '天天基金(东方财富)',
        'object': eastmoney
    },
    {
        'id': 'hsbc',
        'name': '汇丰银行',
        'object': hsbc
    },
    {
        'id': 'csindex',
        'name': '中证指数',
        'object': csindex
    },
    {
        'id': 'bloomberg',
        'name': 'Bloomberg(非内地基金)',
        'object': bloomberg
    },
]


def set_fund_proxy(proxy):
    bloomberg.proxies = {'https': 'http://' + proxy}
