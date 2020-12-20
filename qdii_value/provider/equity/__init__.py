from . import investing_interface, sina_interface

EQUITY_PROVIDER = [
    {
        'id': 'investing',
        'name': '英为财情',
        'object': investing_interface
    },
    {
        'id': 'sina',
        'name': '新浪财经（A/H/美）',
        'object': sina_interface
    },
]


def set_equity_proxy(proxy):
    investing_interface.set_proxy(proxy)
