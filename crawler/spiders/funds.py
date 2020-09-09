import scrapy
from scrapy.http import HtmlResponse
from crawler.items import StockStatus
import random
import demjson


class FundsSpider(scrapy.Spider):
    name = 'funds'
    allowed_domains = ['eastmoney.com', 'investing.com']

    def __init__(self, id, *args, **kwargs):
        super(FundsSpider, self).__init__(*args, **kwargs)
        self.id = id
        self.start_urls = ['http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=' + id +
                           '&topline=50&year=&month=&rt=' +
                           str(random.random())
                           ]

    def parse(self, response):
        rsp = HtmlResponse(url=response.url,
                           body=demjson.decode(response.body.decode(
                               'utf8').split('=', 1)[1][:-1])['content'],
                           encoding='utf-8'
                           )
        lis = []
        for tr in rsp.xpath('.//div[@class="box"][1]//tbody/tr'):
            cur = {'sid': tr.xpath('td[2]//text()').extract_first().rstrip('.HK').rstrip('JP'),
                   'sname': tr.xpath('td[3]//text()').extract_first(),
                   'weight': tr.xpath('td[7]//text()').extract_first(),
                   'volume': tr.xpath('td[8]//text()').extract_first(),
                   'capital': tr.xpath('td[9]//text()').extract_first()
                   }
            movin = yield scrapy.FormRequest(
                url='https://cn.investing.com/search/service/searchTopBar',
                headers={'Referer': 'https://cn.investing.com/',
                        'X-Requested-With': 'XMLHttpRequest'},
                meta={'item': cur},
                formdata={'search_text': cur['sid']},
                callback=self.parse_findstock
            )
            lis.append(cur)
        [print("%-8s %-40s\t%s\t%s\t%s" % (i['sid'], i['sname'],
                                           i['weight'], i['volume'], i['capital'],)) for i in lis]

    def parse_findstock(self, response):
        rsp = demjson.decode(response.body.decode('utf8'))
        if len(rsp['quotes']) == 0:
            return None
        yield scrapy.Request(
            url='https://cn.investing.com' + rsp['quotes'][0]['link'],
            headers={'Referer': 'https://cn.investing.com/'},
            meta={'item': response.meta['item']},
            callback=self.parse_stockprice)

    def parse_stockprice(self, response):
        area = response.xpath(
            './/div[@class="left current-data"]//div[@class="top bold inlineblock"]')
        r = StockStatus()
        item = response.meta['item']
        r['sid'], r['sname'], r['weight'] = item['sid'], item['sname'], item['weight']
        r['current'] = area.xpath('span[1]//text()').extract_first()
        r['delta'] = area.xpath('span[2]//text()').extract_first()
        r['extent'] = area.xpath('span[4]//text()').extract_first()
        yield r
