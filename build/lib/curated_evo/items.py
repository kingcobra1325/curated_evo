
import scrapy


class CuratedEvoItem(scrapy.Item):
    last_updated = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    image_source_url = scrapy.Field()
    sale_price = scrapy.Field()
    orig_price = scrapy.Field()
    available_colors = scrapy.Field()
    available_sizes = scrapy.Field()
    condition = scrapy.Field()
    terrain = scrapy.Field()
    ability_level = scrapy.Field()
    rocker_type = scrapy.Field()
    turning_radius = scrapy.Field()
    waist_width= scrapy.Field()
    flex_rating = scrapy.Field()
    shape = scrapy.Field()
