import argparse, traceback

if __package__:
    from .cli.main import act
else:
    from cli.main import act

parser = argparse.ArgumentParser(description='QDII 基金估值计算')
parser.add_argument('fund_id', type=str, help='基金代码')
parser.add_argument('--proxy', type=str, help='HTTP 代理 (格式: IP 或域名:端口)')

def main():
    args = parser.parse_args()
    try:
        act(args)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()