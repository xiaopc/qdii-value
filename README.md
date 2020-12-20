# qdii-value

估算 QDII 基金的净值

## 注意

- 未考虑汇率等因素

- 数值仅供参考，不作为任何依据

- 投资有风险，操作需谨慎

- 仅供学习交流使用

## 介绍

1. 通过抓取 eastmoney/hsbc 上基金最近的持仓报告，获取持仓前 x 股票代码

2. 在 investing/新浪财经 上查询每只股票当前行情

## 安装

Python 3.6+

```bash
# 使用 pip 安装 (加 -e 参数为本地开发模式)
$ pip install '当前目录'
# 使用 setuptools 安装 (develop 为本地开发模式，--record 输出文件列表)
$ python setup.py install
```

## 使用

**注意：0.3.0 版本起不支持旧版配置文件**

### 命令行界面 CLI

```bash
# 启动脚本
$ qdii-value 基金代码
# 更多参数请参见帮助
$ qdii-value --help
```

### 作为库调用

```python
from qdii_value.confs import Config
from qdii_value import processing

c = Config(json_conf_as_an_object)

equities, summary = processing.fetch(c.data['equities'])
if c.data['reference']:
    reference = processing.single_fetch(c.data['reference'])

# ...
```
