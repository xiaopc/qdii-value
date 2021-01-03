import sys
import os
import string
import enquiries
from datetime import datetime
from dateutil import tz
from .funcs import *

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
        if ret is None or len(ret["equities"]) == 0:
            if enquiries.confirm('未找到持仓信息，需要手动添加吗?'):
                return CustomFundState()
            else:
                return None
        else:
            FUND_CONF = create_conf(ret, FUND_ID)
            FUND_CONF.data["fund_source"] = source
            print('{} ({})'.format(
                FUND_CONF.data["fund_name"], FUND_CONF.data["_id"]))
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
        global FUND_ID, FUND_CONF, FUND_CONF_PATH

        equities, summary, reference = fetch_and_draw(FUND_CONF)
        if enquiries.confirm('需要输出到 CSV 文件吗?'):
            output_csv(FUND_ID.translate(TRANS_TABLE) + '.csv', equities, summary, reference)
        return None


def act(args):
    global FUND_ID

    if args.proxy:
        set_equity_proxy(args.proxy)
        set_fund_proxy(args.proxy)
    FUND_ID = args.fund_id
    state = GetConfigState()
    while state != None:
        state = state.action()
