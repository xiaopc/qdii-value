import argparse

if __package__:
    from .cli.main import act
else:
    from cli.main import act

parser = argparse.ArgumentParser(description='QDII 基金估值计算', formatter_class=argparse.MetavarTypeHelpFormatter)
parser.add_argument('fund_id', type=str, help='基金代码')
parser.add_argument('--update', action='store_true', help='检查持仓表更新 (部分源可能不支持)')
parser.add_argument('--csv', action='store_true', help='保存实时行情至 csv')
parser.add_argument('--history', type=int, help='保存持仓历史数据 (参数: 日, 先阅读 README 再使用)')
parser.add_argument('--proxy', type=str, help='HTTP 代理 (格式: IP 或域名:端口)')

def main():
    act(parser.parse_args())

if __name__ == '__main__':
    main()