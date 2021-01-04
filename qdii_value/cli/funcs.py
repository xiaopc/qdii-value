import sys
import os
import enquiries
from rich import box
from rich.console import Console
from rich.table import Column, Table
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import processing
from provider.equity import *
from provider.fund import *
from confs import Config, _equity


CUR_EQ_PROVIDER = EQUITY_PROVIDER[0]


def clear_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def read_conf(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return Config(obj=f.read())
    else:
        return None


def create_conf(obj, _id):
    c = Config(_id=_id)
    c.data.update(obj)
    return c


def get_fund(_id):
    global FUND_PROVIDER_CN, FUND_PROVIDER_GL
    ret = None
    provider = FUND_PROVIDER_CN if _id.isdigit() else FUND_PROVIDER_GL
    try:
        for f in provider:
            ret = f.lists(_id)
            if ret:
                return f.__name__.split('.')[-1], ret
    except:
        print('查询时出现故障.')
    return None, None


def search_equity(default_query=None):
    global EQUITY_PROVIDER, CUR_EQ_PROVIDER
    data = None
    while data is None:
        default_info = f', 默认: {default_query}' if default_query else ''
        query = input(f'搜索 (p 跳过, q 切换源{default_info}): ') or default_query
        clear_line()
        if query == 'p':
            print('已跳过.')
            return None
        elif query == 'q':
            options = ['{} ({})'.format(p['name'], p['id'])
                       for p in EQUITY_PROVIDER]
            choice = enquiries.choose('上下键选择行情信息源:', options)
            CUR_EQ_PROVIDER = EQUITY_PROVIDER[options.index(choice)]
            continue
        else:
            try:
                search_res = CUR_EQ_PROVIDER['object'].search(query)
            except:
                print('网络错误.')
                continue
            if search_res is None or len(search_res) == 0:
                print('未搜索到结果.')
                continue
            options = list(map(lambda r: '{} | {} ({})'.format(
                r['type'], r['name'], r['code']), search_res[:10]))
            options.append('重新搜索')
            choice = enquiries.choose('上下键选择对应的项目:', options)
            if choice == '重新搜索':
                continue
            print('选中: {}'.format(choice))
            data = search_res[options.index(choice)]
    return {'source': CUR_EQ_PROVIDER['id'], 'source_id': data['source_id'], 'name': data['name'], 'code': data['code']}


def get_equity_list(conf):
    for item in conf.data['equities']:
        print('代码: {}  名称：{}  权重: {}'.format(
            item['code'], item['name'], item['weight']))
        ret = search_equity(item['code'].split('.')[0].split(':')[0] if item['code'] else item['name'])
        if ret is None:
            continue
        item.update(ret)
    conf.data['equities'] = list(
        filter(lambda e: 'source' in e.keys(), conf.data['equities']))


def custom_equities():
    equities = []
    print('添加持仓信息：')
    while True:
        ret = search_equity()
        if ret:
            ret['weight'] = input('权重(百分比, 不加%): ') or '0'
            try:
                float(ret['weight'])
            except:
                print('不是合法的数字, 请重试.\n')
                continue
            equities.append(ret)
            print()
        else:
            break
    return equities


def remove_col_suffix(table, col, suffix):
    l = len(list(filter(lambda a: a[col].endswith(suffix), table)))
    if l == len(table):
        for row in table:
            row[col] = row[col][:-len(suffix)]

def red_green(num, fmt):
    if num > 0:
        return '[bright_red]' + fmt.format(num) + '[/bright_red]'
    elif num < 0:
        return '[bright_green]' + fmt.format(num) + '[/bright_green]'
    else:
        return fmt.format(num)


def fetch_and_draw(conf):
    equities, summary = processing.fetch(conf.data['equities'])
    reference = processing.single_fetch(
        conf.data['reference']) if conf.data['reference'] else None

    caption = '(报价截至 {}, 持仓截至 {})\n'.format(summary['last_update'].strftime(
        '%Y-%m-%d %H:%M:%S'), conf.data['last_update'])
    table = Table(title=conf.data['fund_name'], 
                  caption=caption, caption_style='white', caption_justify='right',
                  box=box.ROUNDED, show_footer=True)

    footer_name = '总计'
    footer_weight = '{:.2f}%'.format(summary['total_weight'])
    footer_current = ''
    footrt_change = ''
    footer_precent = red_green(summary['total_percent'], '{:+.2f}%')
    if summary['today_weight'] > 0 and summary['today_weight'] != summary['total_weight']:
        footer_name += '\n今日交易'
        footer_weight += '\n' + '{:.2f}%'.format(summary['today_weight'])
        footer_current += '\n'
        footrt_change += '\n'
        footer_precent += '\n' + red_green(summary['today_percent'], '{:+.2f}%')
    if reference:
        footer_name += '\n' + reference['name']
        footer_weight += '\n'
        footer_current += '\n' + '{:.2f}'.format(reference['last'])
        footrt_change += '\n' + red_green(reference['change'], '{:+.2f}')
        footer_precent += '\n' + red_green(reference['change_percent'], '{:+.2f}%')

    table.add_column("代码", justify="right", no_wrap=True)
    table.add_column("名称", justify="left",  no_wrap=False, footer=footer_name)
    table.add_column("权重", justify="right", no_wrap=True,  footer=footer_weight)
    table.add_column("当前", justify="right", no_wrap=True,  footer=footer_current)
    table.add_column("涨跌", justify="right", no_wrap=True,  footer=footrt_change)
    table.add_column("幅度", justify="right", no_wrap=True,  footer=footer_precent)

    rows = []
    for i in equities:
        rows.append([
            i['code'],
            ('\U0001f504' if i['is_open'] else '') + i['name'],
            '{:.2f}%'.format(i['weight']),
            '{:.2f}'.format(i['last']),
            red_green(i['change'], '{:+.2f}'),
            red_green(i['change_percent'], '{:+.2f}%'),
        ])
        if 'after_hour_percent' in i.keys():
            rows.append(['', '', '延时', '{:.2f}'.format(i['after_hour_price']),
                         red_green(i['after_hour_change'], '{:+.2f}'), red_green(i['after_hour_percent'], '{:+.2f}%')])

    remove_col_suffix(rows, 3, '.00')
    remove_col_suffix(rows, 4, '.00')
    [table.add_row(*row) for row in rows]
    print()
    console = Console()
    console.print(table)
    return equities, summary, reference


def output_csv(path, equities, summary, reference):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
                                'code', 'name', 'weight', 'last', 'change', 'change_percent'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(equities)
        writer.writerow({'code': '总计', 'name': '', 'weight': summary['total_weight'],
                         'last': '', 'change': '', 'change_percent': summary['total_percent']})
        if summary['today_weight'] > 0 and summary['today_weight'] != summary['total_weight']:
            writer.writerow({'code': '本交易日', 'name': '', 'weight': summary['today_weight'],
                             'last': '', 'change': '', 'change_percent': summary['today_percent']})
        if reference:
            writer.writerow({'code': reference['name'], 'name': '', 'weight': '', 'last': reference['last'],
                             'change': reference['change'], 'change_percent': reference['change_percent']})
        print('已保存至 ' + path + '.')
