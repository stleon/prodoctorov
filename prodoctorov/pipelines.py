# -*- coding: utf-8 -*-


def clear_float(value):
    value = value.strip()
    for i in ('+', '-', u'−'):
        value = value.replace(i, '')
    return float(value) if len(value) > 1 else 0


class DoctorPipeline(object):
    def process_item(self, item, spider):
        if not item['rating']:
            item['rating'] = ''
        item['views'] = int(item['views'])
        item['profession'] = ','.join(item['profession'])
        if item['grade'] == u'степень неизвестна':
            item['grade'] = u'неизвестна'
        item['experience'] = item['experience'].replace(u'стаж', '')
        item['recommend'] = clear_float(item['recommend'])
        item['effectiveness'] = clear_float(item['effectiveness'])
        item['informing'] = clear_float(item['informing'])
        item['quality'] = clear_float(item['quality'])
        item['attitude'] = clear_float(item['attitude'])
        item['sms']['plus'] = int(clear_float(item['sms']['plus']))
        item['sms']['minus'] = int(clear_float(item['sms']['minus']))
        return item
