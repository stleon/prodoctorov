import scrapy
from prodoctorov.items import DoctorItem, SMSItem, InfoItem


def get_next_page(seq):
    for i in seq:
        if 'vrach' not in i:
            return i
    return None


class DoctorsSpider(scrapy.Spider):
    name = "doctors"

    def start_requests(self):
        urls = ['https://prodoctorov.ru/moskva/vrach/#all_spec', ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.professions_parse)

    def professions_parse(self, response):
        professions = response.xpath(
            '//*[@id="content"]/div[1]/div/div[5]/div/ul/li/ul/li/a/@href'
        ).extract()
        for profession in professions:
            if profession != '#all_spec':
                url = response.urljoin(profession)
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        for href in response.xpath(
                '//a[contains(@class, "fio")]/@href').extract():
            yield scrapy.Request(
                response.urljoin(href), callback=self.parse_doctor)

        resp = response.xpath('//span[@class="page"]/a/@href').extract()
        next_page = get_next_page(resp)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.log('=' * 80)
            self.log(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_doctor(self, response):
        stepen = response.xpath('//div[@class="label"]/text()')
        info = InfoItem()
        item = DoctorItem()
        sms = SMSItem()
        city = response.xpath('//*[@id="town"]/text()').extract_first()

        sms['plus'] = response.xpath(
            '//div[@class="smsplus"]/text()').extract_first()
        # TODO format here
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
        # TODO if not raiting == foo bar
        item['rating'] = response.xpath(
            '//*[@id="menu"]/div[1]/div[2]/span/text()').extract_first()
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
