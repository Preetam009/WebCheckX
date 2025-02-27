import scrapy


class WebcheckerSpider(scrapy.Spider):
    name = "webchecker"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
