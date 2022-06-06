from curated_evo.spider_templates import EvoSpider

class SkiPolesSpider(EvoSpider):
    name = 'Ski_Poles'
    start_urls = ['https://www.evo.com/shop/ski/poles']

    item_measurement = 'in'

    excluded_data = [
                    # ski / snowboard
                    "terrain",
                    "ability_level",
                    "rocker_type",
                    # ski only
                    "turning_radius",
                    "waist_width",
                    # snowboard only
                    "flex_rating",
                    "shape",
                    ]