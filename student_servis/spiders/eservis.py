import scrapy
from scrapy.http import FormRequest
from scrapy import Request


class EservisSpider(scrapy.Spider):
    name = 'eservis'
    allowed_domains = ['studentski-servis.com/index.php?t=prostaDela',
                       'studentski-servis.com',
                       'studentski-servis.com/ess/login.php']

    start_urls = ['https://www.studentski-servis.com/ess/login.php', ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                                         formdata={"username": "",
                                                   "password": ""},
                                         callback=self.after_login)

    def after_login(self, response):
        yield scrapy.Request('https://www.studentski-servis.com/index.php?t=prostaDela&regija[]=101&regija[]=002&regija[]=003&regija[]=020&regija[]=021&hp=true&page=1&perPage=10&sort=1&workType=1&keyword=',
                       callback=self.parse_container)

    def parse_container(self, response):
        jobs = response.xpath("//*[@class='jobItem']")

        for page in range(1, 65):
            next_page = "https://studentski-servis.com/index.php?t=prostaDela&regija[]=101&regija[]=002&regija[]=003&regija[]=020&regija[]=021&hp=true&page=" + str(page) + "&perPage=10&sort=1&workType=1&keyword="

            for job in jobs:
                contact = job.xpath(".//*[@class='button button1']/@href").extract()
                ls = ''.join(contact)
                yield scrapy.Request(ls, callback=self.paragraph)
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse_container)



    def paragraph(self, response):
        paragraph = response.xpath("//p/text()").extract()
        yield {"paragraph": paragraph}