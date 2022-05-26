from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from curated_evo.spiders.Skis import SkisSpider
from curated_evo.spiders.Ski_Boots import SkiBootsSpider
from curated_evo.spiders.Ski_Poles import SkiPolesSpider
from curated_evo.spiders.Ski_Helmets import SkiHelmetsSpider
from curated_evo.spiders.Ski_Googles import SkiGooglesSpider
from curated_evo.spiders.Snowboards import SnowboardsSpider
from curated_evo.spiders.Snowboard_Jackets import SnowboardJacketsSpider
from curated_evo.spiders.Snowboard_Pants import SnowboardPantsSpider

spider_list = [
                SkisSpider,
                SkiBootsSpider,
                SkiPolesSpider,
                SkiHelmetsSpider,
                SkiGooglesSpider,
                SnowboardsSpider,
                SnowboardJacketsSpider,
                SnowboardPantsSpider,
            ]



configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    for spider in spider_list:
        yield runner.crawl(spider)
    reactor.stop()

crawl()
reactor.run()