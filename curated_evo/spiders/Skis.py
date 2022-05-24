import scrapy

import curated_evo.env_vars
import curated_evo.dataframes
import curated_evo.missing_modules

class SkisSpider(scrapy.Spider):
    name = 'Skis'
    allowed_domains = ['www.evo.com']
    start_urls = ['http://www.evo.com/']

    def parse(self, response):
        pass
