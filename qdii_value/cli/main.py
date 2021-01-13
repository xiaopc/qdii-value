import sys
import os
import string
import time
import enquiries
from rich.live import Live
from datetime import datetime
from dateutil import tz
from .funcs import *

ARGS = None
FUND_ID, FUND_CONF = None, None
FUND_CONF_PATH = '{}.json'
TRANS_TABLE = ''.maketrans(string.punctuation, '_' * len(string.punctuation))

class State:
    def action(self):
        raise NotImplementedError()


class GetConfigState(State):
    def action(self):
        global FUND_ID, FUND_CONF, FUND_CONF_PATH, TRANS_TABLE

        FUND_CONF = read_conf(FUND_CONF_PATH.format(FUND_ID.translate(TRANS_TABLE)))
        if FUND_CONF:
            print('已读取配置, 如需更新持仓表请删除 {}.'.format(
                FUND_CONF_PATH.format(FUND_ID.translate(TRANS_TABLE))))
            return ListingState()
        else:
            return FindFundState()


class FindFundState(State):
    def action(self):
        global FUND_ID, FUND_CONF, FUND_CONF_PATH

        print('正在获取 {} 持仓信息...'.format(FUND_ID))
        source, ret = get_fund(FUND_ID)
        if source is None:
            return CustomFundState()
        else:
            FUND_CONF = create_conf(ret, FUND_ID)
            FUND_CONF.data["fund_source"] = source
            print('{} ({})'.format(FUND_CONF.data["fund_name"], FUND_CONF.data["_id"]))
            if FUND_CONF.data["last_update"]:
                print('持仓截至: ' + FUND_CONF.data["last_update"])
            get_equity_list(FUND_CONF)
            return FinishAddState()


class CustomFundState(State):
    def action(self):
        global FUND_ID, FUND_CONF, FUND_CONF_PATH

        now = datetime.now(tz=tz.gettz('Asia/Shanghai'))
        ret = {'fund_name': input('请输入组合名: '),
               'last_update': now.strftime('%Y-%m-%d'),
               'equities': custom_equities()}
        FUND_CONF = create_conf(ret, FUND_ID)
        return FinishAddState()


class FinishAddState(State):
    def action(self):
        global FUND_ID, FUND_CONF, FUND_CONF_PATH

        if enquiries.confirm('需要增加参考指数吗?'):
            FUND_CONF.data['reference'] = search_equity()
        ret = FUND_CONF.save(FUND_CONF_PATH.format(FUND_ID.translate(TRANS_TABLE)))
        print(f'配置已保存至 {ret}, 如需更新持仓表请删除文件.')
        return ListingState()


class ListingState(State):
    def action(self):
        global ARGS, FUND_ID, FUND_CONF, FUND_CONF_PATH

        if ARGS.history:
            history_csv(FUND_ID.translate(TRANS_TABLE) + f'_{ARGS.history}d.csv', FUND_CONF, ARGS.history)
        elif ARGS.csv:
            equities, summary, reference = fetch_data(FUND_CONF)
            output_csv(FUND_ID.translate(TRANS_TABLE) + '.csv', equities, summary, reference)
        else:
            print()
            with Live(auto_refresh=False) as live:
                while True:
                    equities, summary, reference = fetch_data(FUND_CONF)
                    live.update(get_table(FUND_CONF, equities, summary, reference), refresh=True)
                    time.sleep(10)
        return None


def act(args):
    global FUND_ID, ARGS

    ARGS = args
    if ARGS.proxy:
        set_equity_proxy(ARGS.proxy)
        set_fund_proxy(ARGS.proxy)
    FUND_ID = ARGS.fund_id
    state = GetConfigState()
    while state != None:
        state = state.action()
