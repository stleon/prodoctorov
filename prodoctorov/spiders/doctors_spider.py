import scrapy


class DoctorsSpider(scrapy.Spider):
    name = "doctors"
    start_urls = [
        'https://prodoctorov.ru/moskva/vrach/',
    ]

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "fio")]/@href').extract():
            self.log(href)
            yield scrapy.Request(
                response.urljoin(href), callback=self.parse_doctor)
        '''
        next_page = response.xpath('').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        '''

    def parse_doctor(self, response):
        pass
