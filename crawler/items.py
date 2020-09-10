# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundsPosition(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    stocks = scrapy.Field()
    last_update = scrapy.Field()

class StockStatus(scrapy.Item):
    sid = scrapy.Field()
    sname = scrapy.Field()
    weight = scrapy.Field()

    sname_i = scrapy.Field()
    current = scrapy.Field()
    delta = scrapy.Field()
    extent = scrapy.Field()