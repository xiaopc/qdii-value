import sys
import os
import enquiries
import demjson
from texttable import Texttable
import csv
import eastmoney
import investing

def clear_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

if len(sys.argv) < 2:
    sys.exit('使用方法：python main.py *基金代码*')

data = []
conf_path = sys.argv[1] + '.json'

# confs
if os.path.exists(conf_path):
    with open(conf_path, 'r') as f:
        data = demjson.decode(f.read())
        print('已读取配置, 如需更新持仓表请删除 {}.'.format(conf_path))
else:
    print('正在获取 {} 持仓信息...'.format(sys.argv[1]))
    lis = eastmoney.lists(sys.argv[1])
    if len(lis) == 0:
        sys.exit('未找到持仓信息.')
    print('开始匹配行情信息.')
    for item in lis:
        print('代码: {}  名称：{}  权重: {}'.format(item['sid'], item['name'], item['weight']))
        while True:
            query = input('搜索关键字，按 p 跳过(默认: {}): '.format(item['sid'])) or item['sid']
            clear_line()
            if query == 'p':
                print('已跳过.')
                break
            search_res = investing.search(query)
            if search_res is None or len(search_res) == 0:
                print('未搜索到结果.')
                continue
            options = list(map(lambda r: '{} | {}'.format(r['search_main_subtext'], r['search_main_longtext']), search_res[:10]))
            options += ['重新搜索']
            choice = enquiries.choose('上下选择对应的股票:', options)
            if choice == '重新搜索':
                continue
            print('选中: {}'.format(choice))
            item['source'] = 'investing'
            item['investing_pairid'] = search_res[options.index(choice)]['pair_ID']
            data.append(item)
            break
        print()
    with open(conf_path, 'w') as f:
        f.write(demjson.encode(data))
        print('配置已保存至 {}, 如需更新持仓表请删除文件.'.format(conf_path))

# status
pair_ids = list(map(lambda x: x['investing_pairid'], data))
res = investing.lists(pair_ids)
total_weight, total_percent = 0., 0.
for item in data:
    item_w = float(item['weight'][:-1]) / 100
    item_res = filter(lambda r: r['pair_ID'] == item["investing_pairid"], res)
    try:
        status = next(item_res)
        item['last'] = status['last']
        item['change'] = status['change']
        item['change_percent'] = status['change_percent_val']
        item['name_provided'] = status['pair_name']
        total_percent += item_w * float(item['change_percent']) / 100
        total_weight += item_w
    except StopIteration:
        continue

table = Texttable()
table.set_deco(Texttable.BORDER | Texttable.HEADER)
table.header(['代码', '公司', '权重', '当前价', '涨跌', '幅度'])
table.set_cols_dtype(['t','t','t','t','t','t'])
table.set_cols_align(['c', 'l', 'c', 'r', 'r', 'r'])
rows = [[i['sid'], i['name_provided'], i['weight'], i['last'], i['change'], i['change_percent'] + '%'] for i in data]
table.add_rows(rows, header=False)
print(table.draw())
print('持仓表占总资产 {:.2f}%, 估值目前振幅为 {:.2f}%.'.format(total_weight * 100, total_percent * 100))

if enquiries.confirm('需要输出到 CSV 文件吗?'):
    with open(sys.argv[1] + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['sid', 'name_provided', 'weight', 'last', 'change', 'change_percent'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        writer.writerow({'sid': '总计', 'name_provided': '', 'weight': total_weight, 'last': '', 'change': '', 'change_percent': total_percent * 100})

