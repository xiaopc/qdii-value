from . import investing_interface, sina_interface, yahootw_interface, gfinance_interface, msn_interface

EQUITY_PROVIDER = [
    {
        'id': 'sina',
        'name': '新浪财经（A/H/美）',
        'object': sina_interface
    },
    {
        'id': 'investing',
        'name': '英为财情',
        'object': investing_interface
    },
    {
        'id': 'msn',
        'name': '微软 MSN 财经',
        'object': msn_interface
    },
    {
        'id': 'yahootw',
        'name': '雅虎奇摩（台/美）',
        'object': yahootw_interface
    },
    {
        'id': 'gfinance',
        'name': 'Google Finance',
        'object': gfinance_interface
    },
]


def set_equity_proxy(proxy):
    investing_interface.set_proxy(proxy)
    yahootw_interface.set_proxy(proxy)
    gfinance_interface.set_proxy(proxy)
