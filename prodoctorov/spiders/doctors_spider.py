import scrapy
from prodoctorov.items import DoctorItem, SMSItem, InfoItem


def get_next_page(seq):
    for i in seq:
        if 'vrach' not in i:
            return i
    return None


class DoctorsSpider(scrapy.Spider):
    name = "doctors"
    start_urls = ['https://prodoctorov.ru/moskva/vrach/', ]

    def parse(self, response):

        for href in response.xpath(
                '//a[contains(@class, "fio")]/@href').extract():
            yield scrapy.Request(
                response.urljoin(href), callback=self.parse_doctor)

        resp = response.xpath('//span[@class="page"]/a/@href').extract()
        next_page = get_next_page(resp)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.log('='*80)
            self.log(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_doctor(self, response):
        stepen = response.xpath('//div[@class="label"]/text()')
        info = InfoItem()
        item = DoctorItem()
        sms = SMSItem()
        city = response.xpath('//*[@id="town"]/text()').extract_first()

        sms['plus'] = response.xpath(
            '//*[@id="menu"]/div[7]/div/div[1]/text()').extract_first()
        # TODO format here
        sms['minus'] = response.xpath(
            '//*[@id="menu"]/div[7]/div/div[2]/text()').extract_first()

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
            '//*[@id="menu"]/div[1]/div[2]/span/text()').extract_first()
        item['recommend'] = response.xpath(
            '//*[@id="menu"]/div[2]/div[2]/div/text()').extract_first()
        item['effectiveness'] = response.xpath(
            '//*[@id="menu"]/div[3]/div[2]/div/text()').extract_first()
        item['informing'] = response.xpath(
            '//*[@id="menu"]/div[4]/div[2]/div/text()').extract_first()
        item['quality'] = response.xpath(
            '//*[@id="menu"]/div[5]/div[2]/div/text()').extract_first()
        item['attitude'] = response.xpath(
            '//*[@id="menu"]/div[6]/div[2]/div/text()').extract_first()
        item['sms'] = sms
        item['views'] = response.xpath(
            '//*[@id="menu"]/div[9]/div[2]/div/text()').extract_first()
        item['info'] = info

        yield item
