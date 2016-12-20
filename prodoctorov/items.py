# -*- coding: utf-8 -*-

import scrapy


class ProdoctorovItem(scrapy.Item):
    name = scrapy.Field()
    profession = scrapy.Field()
    grade = scrapy.Field()
    category = scrapy.Field()
    experience = scrapy.Field()
    rating = scrapy.Field()
    recommend = scrapy.Field()
    effectiveness = scrapy.Field()
    informing = scrapy.Field()
    quality = scrapy.Field()
    attitude = scrapy.Field()
    sms = scrapy.Field()
    views = scrapy.Field()
    info = scrapy.Field()

