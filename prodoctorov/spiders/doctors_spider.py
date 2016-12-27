import urlparse

import scrapy

from prodoctorov.items import DoctorItem, InfoItem, SMSItem


def parse_page_number(url):
    try:
        return int(urlparse.parse_qs(urlparse.urlparse(url).query)['page'][0])
    except KeyError:
        return 1


def get_next_page(pages, current_page):
    """
    [u'?page=2'], 1
    [u'/moskva/akusher/', u'?page=3'], 2
    [u'/moskva/akusher/?page=3', u'?page=5'], 4
    [u'/moskva/akusher/?page=61'], 62
    """

    for page in pages:
        page_number = parse_page_number(page)
        if page_number > current_page:
            return '?page=%s' % page_number
    return None


class DoctorsSpider(scrapy.Spider):
    name = "doctors"

    def start_requests(self):
        yield scrapy.Request(
            url='https://prodoctorov.ru/ajax/town/moskva/',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            callback=self.parse_city)

    def parse_city(self, response):
        cities = response.xpath('//ul/li/a/@href | //ul/li/b/a/@href').extract(
        )
        for city in cities:
            url = response.urljoin('%svrach/' % city)
            yield scrapy.Request(url=url, callback=self.professions_parse)

    def professions_parse(self, response):
        all_doctors = sum(
            (int(i.strip())
             for i in response.xpath('//span[contains(@class, "cnt")]/text()')
             .extract()))
        self.log('=' * 80)
        self.log(response.url)
        self.log(all_doctors)
        self.log('=' * 80)

        professions = response.xpath(
            '//div[@class="town_vrach_all town_menu active"]/ul/li/ul/li/a/@href'
        ).extract()
        for profession in professions:
            if profession != '#all_spec':
                url = response.urljoin(profession)
                yield scrapy.Request(url, callback=self.parse_doctor_list)

    def parse_doctor_list(self, response):

        for href in response.xpath(
                '//a[contains(@class, "fio")]/@href').extract():
            yield scrapy.Request(
                response.urljoin(href), callback=self.parse_doctor)

        resp = response.xpath('//span[@class="page"]/a/@href').extract()
        next_page = get_next_page(
            pages=resp, current_page=parse_page_number(response.url))

        if next_page is not None:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse)

    def parse_doctor(self, response):
        stepen = response.xpath('//div[@class="label"]/text()')
        info = InfoItem()
        item = DoctorItem()
        sms = SMSItem()
        city = response.xpath('//*[@id="town"]/text()').extract_first()

        sms['plus'] = response.xpath(
            '//div[@class="smsplus"]/text()').extract_first()
        sms['minus'] = response.xpath(
            '//div[@class="smsminus"]/text()').extract_first()

        info['address'] = '%s, %s' % (response.xpath(
            '//*[@id="main"]/div[1]/div[1]/div[1]/div/div[1]/span/span[2]/span/text()'
        ).extract_first(), city)
        info['company'] = response.xpath(
            '//*[@id="main"]/div[1]/div[1]/div[1]/div/div[1]/span/span[2]/a/text()'
        ).extract_first()

        item['name'] = response.xpath(
            '//*[@id="content"]/div[2]/div/div[2]/h1/span/text()'
        ).extract_first()
        item['profession'] = response.xpath(
            '//div[@class="doctor_head_spec"]/a/text()').extract()
        item['grade'] = stepen[0].extract()
        item['category'] = stepen[1].extract()
        item['experience'] = stepen[2].extract()
        item['rating'] = response.xpath(
            '//div[@class="inoval_big"]/span/text()').extract_first()
        item['recommend'] = response.xpath(
            '//div[@class="inoval fon-recommend"]/div/text()').extract_first()
        item['effectiveness'] = response.xpath(
            '//div[@class="inoval fon-results"]/div/text()').extract_first()
        item['informing'] = response.xpath(
            '//div[@class="inoval fon-info"]/div/text()').extract_first()
        item['quality'] = response.xpath(
            '//div[@class="inoval fon-osmotr"]/div/text()').extract_first()
        item['attitude'] = response.xpath(
            '//div[@class="inoval fon-friendliness"]/div/text()'
        ).extract_first()
        item['sms'] = sms
        item['views'] = response.body.split("$('#box .head').html('")[1].split(
            ' ')[0]
        item['info'] = info

        yield item
