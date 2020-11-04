import sys
import argparse
import os
import time
import enquiries
import demjson
from texttable import Texttable
import csv
import eastmoney
import hsbc
import investing

def clear_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def search(query_default=None, return_full=False):
    ret = None
    while True:
        question = '搜索关键字，按 p 结束: ' if query_default is None else '搜索关键字，按 p 跳过(默认: {}): '.format(query_default)
        query = input(question) or query_default or 'p'
        clear_line()
        if query == 'p':
            print('已跳过.')
            break
        try:
            search_res = investing.search(query)
        except:
            print('网络错误.')
            continue
        if search_res is None or len(search_res) == 0:
            print('未搜索到结果.')
            continue
        options = list(map(lambda r: '{} | {} ({})'.format(r['search_main_subtext'], r['search_main_longtext'], r['search_main_text']), search_res[:10]))
        options += ['重新搜索']
        choice = enquiries.choose('上下键选择对应的项目:', options)
        if choice == '重新搜索':
            continue
        print('选中: {}'.format(choice))
        ret = search_res[options.index(choice)]
        ret = ret if return_full else ret['pair_ID']
        break
    if return_full is not True:
        print()
    return ret

parser = argparse.ArgumentParser(description='QDII 基金估值计算')
parser.add_argument('fund_id', type=str, help='基金代码')
parser.add_argument('--proxy', type=str, help='HTTP 代理 (格式: IP或域名:端口)')
args = parser.parse_args()
if args.proxy:
    investing.proxies = {'https': 'http://' + args.proxy}

data = {
    'last_update': None,
    'equities': [],
    'reference': None
}

# confs
conf_path = args.fund_id + '.json'
if os.path.exists(conf_path):
    with open(conf_path, 'r') as f:
        d = demjson.decode(f.read())
    if isinstance(d, list):
        print('发现旧版配置，自动更新...')
        data['last_update'] = int(time.time())
        data['equities'] = d
        with open(conf_path, 'w') as f:
            f.write(demjson.encode(data))
    else:
        data = d
    print('已读取配置, 如需更新持仓表请删除 {}.'.format(conf_path))
else:
    print('正在获取 {} 持仓信息...'.format(args.fund_id))
    lis = eastmoney.lists(args.fund_id) or hsbc.lists(args.fund_id)
    if lis is None or len(lis) == 0:
        if enquiries.confirm('未找到持仓信息，需要手动添加吗?'):
            i = 0
            while True:
                i += 1
                print('添加 # {} 持仓信息:'.format(i))
                item = search(return_full=True)
                if item is None:
                    break
                weight = input('权重(百分比, 加%): ') or '0%'
                data['equities'].append({
                    'source': 'investing', 
                    'investing_pairid': item['pair_ID'], 
                    'name': item['search_main_longtext'], 
                    'sid': item['search_main_text'], 
                    'capital': '', 
                    'volume': '', 
                    'weight': weight
                })
                print()
            if len(data['equities']) == 0:
                sys.exit()
        else:
            sys.exit()
    else:
        print('开始匹配行情信息.')
        for item in lis:
            print('代码: {}  名称：{}  权重: {}'.format(item['sid'], item['name'], item['weight']))
            pair_id = search(item['sid'].split('.')[0])
            if pair_id is None:
                continue
            item['source'] = 'investing'
            item['investing_pairid'] = pair_id
            data['equities'].append(item)
    if enquiries.confirm('需要增加参考指数吗?'):
        item = search(return_full=True)
        if item is not None:
            data['reference'] = {
                'source': 'investing', 
                'investing_pairid': item['pair_ID'], 
                'name': item['search_main_longtext'], 
                'sid': item['search_main_text']
            }
    data['last_update'] = int(time.time())
    with open(conf_path, 'w') as f:
        f.write(demjson.encode(data))
        print('配置已保存至 {}, 如需更新持仓表请删除文件.'.format(conf_path))

# status
pair_ids = list(map(lambda x: x['investing_pairid'], data['equities']))
res = investing.lists(pair_ids)
total_weight, total_percent = 0., 0.
for item in data['equities']:
    item_w = float(item['weight'][:-1]) / 100
    item_res = filter(lambda r: r['pair_ID'] == item["investing_pairid"], res)
    try:
        status = next(item_res)
        item['open'] = status['exchange_is_open']
        item['last'] = status['last']
        item['change'] = status['change']
        item['change_percent'] = status['change_percent_val']
        item['name_provided'] = status['pair_name']
        total_percent += item_w * float(item['change_percent']) / 100
        total_weight += item_w
    except StopIteration:
        continue
total_percent /= total_weight

# show table
table = Texttable()
table.set_deco(Texttable.BORDER | Texttable.HEADER)
table.header(['代码', '公司', '权重', '当前价', '涨跌', '幅度'])
table.set_cols_dtype(['t','t','t','t','t','t'])
table.set_cols_align(['r', 'l', 'c', 'r', 'r', 'r'])
rows = [[i['sid'], i['name_provided'], i['weight'], i['last'] + ('\U0001f504' if i['open'] else ''), i['change'], i['change_percent'] + '%'] for i in data['equities']]
table.add_rows(rows, header=False)
print(table.draw())
print('持仓表占总资产 {:.2f}%, 估值目前振幅为 {:.2f}%.'.format(total_weight * 100, total_percent * 100))

# reference
ref = None
if data['reference'] is not None:
    ref = investing.lists([data['reference']['investing_pairid']])[0]
    print('参考: {} 目前 {} 点, {}{}.'.format(data['reference']['name'], ref['last'], ref['change'], ref['change_precent']))

# export to csv
if enquiries.confirm('需要输出到 CSV 文件吗?'):
    with open(args.fund_id + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['sid', 'name_provided', 'weight', 'last', 'change', 'change_percent'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data['equities'])
        writer.writerow({'sid': '总计', 'name_provided': '', 'weight': total_weight, 'last': '', 'change': '', 'change_percent': total_percent * 100})
        if ref:
            writer.writerow({'sid': data['reference']['name'], 'name_provided': '', 'weight': '', 'last': ref['last'], 'change': ref['change'], 'change_percent': ref['change_percent_val']})
        print('已保存至 ' + args.fund_id + '.csv.')

