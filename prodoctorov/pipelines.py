# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProdoctorovPipeline(object):
    def process_item(self, item, spider):
        item['views'] = int(item['views'].strip()[:-1])
        item['profession'] = ','.join(item['profession'])
        if item['grade'] == u'степень неизвестна':
            item['grade'] = u'неизвестна'
        item['experience'] = item['experience'].replace(u'стаж', '')
        for i in ('+', '-'):
            item['recommend'] = item['recommend'].replace(i, '')
        item['recommend'] = float(item['recommend'])
        return item
