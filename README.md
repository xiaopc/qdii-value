# qdii-value

估算 QDII 基金的净值

## 注意

- 未考虑汇率等因素

- 数值仅供参考，不作为任何依据

- 投资有风险，操作需谨慎

- 仅供学习交流使用

## 介绍

1. 通过抓取 eastmoney/hsbc 上基金最近的持仓报告，获取持仓前 x 股票代码

2. 在 investing.com 上查询每只股票当前行情

## 使用

Python 3.5+

```bash
# 安装依赖
pip install -r requirements.txt
# 启动脚本
python main.py 基金代码
# 更多参数请参见帮助
python main.py --help
```
