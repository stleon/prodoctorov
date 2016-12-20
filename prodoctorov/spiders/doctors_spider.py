import scrapy


class DoctorsSpider(scrapy.Spider):
    name = "doctors"
    start_urls = ['https://prodoctorov.ru/moskva/vrach/', ]

    def parse(self, response):
        for href in response.xpath(
                '//a[contains(@class, "fio")]/@href').extract():
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
        stepen = response.xpath('//div[@class="label"]/text()')
        sms = {}
        info = {}
        sms['plus'] = response.xpath(
            '//*[@id="menu"]/div[7]/div/div[1]/text()').extract_first()
        # TODO format here
        sms['minus'] = response.xpath(
            '//*[@id="menu"]/div[7]/div/div[2]/text()').extract_first()

        info['address'] = response.xpath(
            '//*[@id="main"]/div[1]/div[1]/div[1]/div/div[1]/span/span[2]/span/text()'
        ).extract_first()
        info['company'] = response.xpath(
            '//*[@id="main"]/div[1]/div[1]/div[1]/div/div[1]/span/span[2]/a/text()'
        ).extract_first(),
        yield {
            'name': response.xpath(
                '//*[@id="content"]/div[2]/div/div[2]/h1/span/text()').extract(
                ),
            'profession': response.xpath(
                '//*[@id="content"]/div[2]/div/div[2]/div[1]/a/text()')
            .extract(),
            'grade': stepen[0].extract(),
            'category': stepen[1].extract(),
            'experience': stepen[2].extract(),
            'rating': response.xpath(
                '//*[@id="menu"]/div[1]/div[2]/span/text()').extract_first(),
            'recommend': response.xpath(
                '//*[@id="menu"]/div[2]/div[2]/div/text()').extract_first(),
            'effectivenessv': response.xpath(
                '//*[@id="menu"]/div[3]/div[2]/div/text()').extract_first(),
            'informing': response.xpath(
                '//*[@id="menu"]/div[4]/div[2]/div/text()').extract_first(),
            'quality': response.xpath(
                '//*[@id="menu"]/div[5]/div[2]/div/text()').extract_first(),
            'attitude': response.xpath(
                '//*[@id="menu"]/div[6]/div[2]/div/text()').extract_first(),
            'sms': sms,
            'views': response.xpath('//*[@id="menu"]/div[9]/div[2]/div/text()')
            .extract_first().strip()[:-1],
            'city': response.xpath('//*[@id="town"]/text()').extract_first(),
            'info': info,
        }
