import scrapy

class ScrapperItem(scrapy.Item):
    url = scrapy.Field()
    endpoint_url = scrapy.Field()
    tnc_value = scrapy.Field()
    privacy_value = scrapy.Field()
    href_lang = scrapy.Field()
    youtube_value = scrapy.Field()
    gtm_code = scrapy.Field()
    ssl_certificate = scrapy.Field()
    sitemap_value = scrapy.Field()
    
class InactiveItme(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
