from . import eastmoney, hsbc, bloomberg

FUND_PROVIDER_CN = [eastmoney, hsbc]
FUND_PROVIDER_GL = [bloomberg]

def set_fund_proxy(proxy):
    bloomberg.proxies = {'https': 'http://' + proxy}
