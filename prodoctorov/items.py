# -*- coding: utf-8 -*-

import scrapy


class SMSItem(scrapy.Item):
    plus = scrapy.Field()
    minus = scrapy.Field()


class InfoItem(scrapy.Item):
    address = scrapy.Field()
    company = scrapy.Field()


class DoctorItem(scrapy.Item):
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
    views = scrapy.Field()
    sms = scrapy.Field(serializer=SMSItem)
    info = scrapy.Field(serializer=InfoItem)
