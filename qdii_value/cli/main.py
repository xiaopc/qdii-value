import string
import time
import inquirer
from rich.live import Live
from rich.console import Console
from datetime import datetime
from dateutil import tz
from .funcs import *

ARGS = None
FUND_ID, FUND_CONF, OLD_FUND_CONF = None, None, None
FUND_CONF_PATH = '{}.json'
TRANS_TABLE = ''.maketrans(string.punctuation, '_' * len(string.punctuation))


class State:
    def action(self):
        raise NotImplementedError()


class GetConfigState(State):
    def action(self):
        global ARGS, FUND_ID, FUND_CONF, FUND_CONF_PATH, TRANS_TABLE

        FUND_CONF = read_conf(FUND_CONF_PATH.format(FUND_ID.translate(TRANS_TABLE)))
        if FUND_CONF and not ARGS.update:
            print('已读取配置, 更新持仓表可添加 --update 参数.')
            return ListingState()
        else:
            return FindFundState()


class FindFundState(State):
    def action(self):
        global ARGS, FUND_ID, FUND_CONF, OLD_FUND_CONF, FUND_CONF_PATH

        print('正在获取 {} 持仓信息...'.format(FUND_ID))
        if ARGS.update and FUND_CONF and FUND_CONF.data['fund_source']:
            provider = get_fund_provider(FUND_CONF.data['fund_source'])
        else:
            provider = get_fund_provider()
            if provider is False:
                return CustomFundState()
        ret = get_fund(FUND_ID, provider)
        if ret:
            if ARGS.update and FUND_CONF and FUND_CONF.data['last_update'] == ret['last_update']:
                print(f'{FUND_ID} 暂无更新.')
                return ListingState()
            elif ARGS.update and FUND_CONF:
                print(f'发现 {FUND_ID} 发布新持仓, 开始更新.')
            OLD_FUND_CONF = FUND_CONF
            FUND_CONF = create_conf(ret, FUND_ID)
            FUND_CONF.data["fund_source"] = provider['id']
            print('{} ({})'.format(FUND_CONF.data["fund_name"], FUND_CONF.data["_id"]))
            if FUND_CONF.data["last_update"]:
                print('持仓截至: ' + FUND_CONF.data["last_update"])
            return UpdateEquityState()
        else:
            return None

class UpdateEquityState(State):
    def action(self):
        global FUND_CONF, OLD_FUND_CONF
        for item in FUND_CONF.data['equities']:
            print('\n代码: {}  名称：{}  权重: {}'.format(item['code'], item['name'], item['weight']))
            placeholder = item['code'].split('.')[0].split(':')[0] if item['code'] else None
            exist_item = list(filter(lambda i: i['code'] == placeholder or i['name'] == item['name'], OLD_FUND_CONF.data['equities'])) if OLD_FUND_CONF is not None else []
            if len(exist_item) > 0 and inquirer.confirm(message='之前的匹配: {}({})，使用吗?'.format(exist_item[0]['name'], exist_item[0]['code'])):
                item.update({
                    'source': exist_item[0]['source'],
                    'source_id': exist_item[0]['source_id'],
                    'name': exist_item[0]['name'],
                    'code': exist_item[0]['code']
                })
                clear_line()
                continue
            ret = search_equity(placeholder if placeholder else item['name'])
            if ret is None:
                continue
            item.update(ret)
        FUND_CONF.data['equities'] = list(filter(lambda e: 'source' in e.keys(), FUND_CONF.data['equities']))
        return FinishAddState()


class CustomFundState(State):
    def action(self):
        global FUND_ID, FUND_CONF, FUND_CONF_PATH

        now = datetime.now(tz=tz.gettz('Asia/Shanghai'))
        todaystr = now.strftime('%Y-%m-%d')
        ret = {'fund_name': input('输入组合名: '),
               'last_update': input(f'输入日期(默认 {todaystr}): ') or todaystr,
               'equities': custom_equities()}
        FUND_CONF = create_conf(ret, FUND_ID)
        return FinishAddState()


class FinishAddState(State):
    def action(self):
        global FUND_ID, FUND_CONF, OLD_FUND_CONF, FUND_CONF_PATH

        if len(FUND_CONF.data['equities']) == 0:
            raise UserWarning("没有添加任何持仓")
        if OLD_FUND_CONF is not None and OLD_FUND_CONF.data['reference'] and inquirer.confirm(message='保留原参考指数吗?'):
            FUND_CONF.data['reference'] = OLD_FUND_CONF.data['reference']
        elif inquirer.confirm(message='需要增加参考指数吗?'):
            FUND_CONF.data['reference'] = search_equity()
        ret = FUND_CONF.save(FUND_CONF_PATH.format(FUND_ID.translate(TRANS_TABLE)))
        print(f'配置已保存至 {ret}, 更新持仓表可添加 --update 参数.')
        return ListingState()


class ListingState(State):
    def action(self):
        global ARGS, FUND_ID, FUND_CONF, FUND_CONF_PATH

        if len(FUND_CONF.data['equities']) == 0:
            raise UserWarning("没有添加任何持仓")
        if ARGS.history:
            history_csv(FUND_ID.translate(TRANS_TABLE) + f'_{ARGS.history}d.csv', FUND_CONF, ARGS.history)
        elif ARGS.csv:
            output_csv(FUND_ID.translate(TRANS_TABLE) + '.csv', *fetch_data(FUND_CONF))
        else:
            with Live(auto_refresh=False, redirect_stdout=False) as live:
                while True:
                    live.update(get_table(FUND_CONF, *fetch_data(FUND_CONF)), refresh=True)
                    time.sleep(10)
        return None


def act(args):
    global FUND_ID, ARGS

    console = Console()
    try:
        ARGS = args
        if ARGS.proxy:
            set_equity_proxy(ARGS.proxy)
            set_fund_proxy(ARGS.proxy)
        FUND_ID = ARGS.fund_id
        state = GetConfigState()
        while state is not None:
            state = state.action()
    except KeyboardInterrupt:
        pass
    except:
        console.print_exception()
