import scrapy
from scrapy.http import HtmlResponse
from crawler.items import StockStatus
import random
import re
import demjson
import cfscrape

class FundsSpider(scrapy.Spider):
    name = 'funds'
    allowed_domains = ['eastmoney.com', 'investing.com']

    def __init__(self, id, exchange=None, id_len=None, name_conv=False, *args, **kwargs):
        super(FundsSpider, self).__init__(*args, **kwargs)
        self.id = id
        self.exchange = exchange
        self.id_len = None if id_len is None else int(id_len) # 取代码最后 x 位，为了处理 eastmoney 在前面乱加 0 的 问题
        self.name_conv = name_conv

        self.investing_type = '股票 '
        self.sk_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/vnd.api+json',
            'Referer': 'https://www.smartkarma.com/insights'
        }
        self.scraper = cfscrape.create_scraper()
        self.start_urls = ['http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=' + id +
                           '&topline=50&year=&month=&rt=' +
                           str(random.random())
                           ]

    def parse(self, response):
        rsp = HtmlResponse(url=response.url,
                           body=demjson.decode(response.body.decode('utf8').split('=', 1)[1][:-1])['content'],
                           encoding='utf-8'
                           )
        lis = []
        for tr in rsp.xpath('.//div[@class="box"][1]//tbody/tr'):
            cur = {'sid': tr.xpath('td[2]//text()').extract_first(),
                   'sname': tr.xpath('td[3]//text()').extract_first(),
                   'weight': tr.xpath('td[7]//text()').extract_first(),
                   'volume': tr.xpath('td[8]//text()').extract_first(),
                   'capital': tr.xpath('td[9]//text()').extract_first()
                   }
            if self.id_len is not None:
                cur['sid'] = re.findall("\d+", cur['sid'])[0][-self.id_len:]
            elif self.name_conv:
                prettier = self.parse_get_prettier(cur['sid'])
                if prettier is not None:
                    pretty_name = prettier['pretty-name']
                    cur['sname'] += '(' + pretty_name + ')'
                else:
                    pretty_name = None
            
            if not self.name_conv or pretty_name is not None:
                movin = yield scrapy.FormRequest(
                    url='https://cn.investing.com/search/service/searchTopBar',
                    headers={'Referer': 'https://cn.investing.com/',
                            'X-Requested-With': 'XMLHttpRequest'},
                    meta={'item': cur},
                    formdata={'search_text': pretty_name if self.name_conv else cur['sid']},
                    callback=self.parse_find_stock
                )
            lis.append(cur)
        print('=' * 43 + ' 持仓表 ' + '=' * 43)
        [print("%-10s %-50s\t%s\t%s\t%s" % (i['sid'], i['sname'],
                                           i['weight'], i['volume'], i['capital'],)) for i in lis]
        print('=' * 93)

    def parse_get_prettier(self, sid):
        # 本函数非 Scrapy 
        # {
        #     bbgid: "..."
        #     country: "United States"
        #     logo-url: {...}
        #     pretty-name: "Prologis Inc"
        #     search-highlight: null
        #     sector: "Real Estate"
        #     security: "PLD US EQUITY"
        #     short-name: "Prologis Inc"
        #     slug: "prologis-inc"
        #     yahoo-ticker: "PLD"
        # }
        url = "https://www.smartkarma.com/api/v2/search?include=primary-entity%2Ccompany&page%5Bnumber%5D=1&page%5Bsize%5D=12&query-text=" + sid + "&search-type=quick"
        rsp = demjson.decode(self.scraper.get(url, headers=self.sk_headers).content)
        entities = filter(lambda q: q['type'] == 'entities', rsp['data'])
        try:
            entity = next(entities)
            print("c: %s => %s" % (sid, entity['attributes']['pretty-name']))
            return entity['attributes']
        except StopIteration:
            return None

    def parse_find_stock(self, response):
        rsp = demjson.decode(response.body.decode('utf8'))
        l = lambda q: self.investing_type in q['type'] and (self.exchange is None or self.exchange in q['exchange'])
        quotes = filter(l, rsp['quotes'])
        try:
            quote = next(quotes)
            print("i: %-8s %-40s\t%s\t%s" % (quote['symbol'], quote['name'], quote['type'], quote['link']))
            yield scrapy.Request(
                url='https://cn.investing.com' + quote['link'],
                headers={'Referer': 'https://cn.investing.com/'},
                meta={'item': response.meta['item'], 'quote': quote},
                callback=self.parse_stock_price)
        except StopIteration:
            return None

    def parse_stock_price(self, response):
        area = response.xpath(
            './/div[@class="left current-data"]//div[@class="top bold inlineblock"]')
        r = StockStatus()
        item = response.meta['item']
        r['sid'], r['sname'], r['weight'] = item['sid'], item['sname'], item['weight']
        r['sname_i'] = response.meta['quote']['name']
        r['current'] = area.xpath('span[1]//text()').extract_first()
        r['delta'] = area.xpath('span[2]//text()').extract_first()
        r['extent'] = area.xpath('span[4]//text()').extract_first()
        yield r
