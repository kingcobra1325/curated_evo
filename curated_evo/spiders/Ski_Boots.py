from curated_evo.spider_templates import EvoSpider

class SkiBootsSpider(EvoSpider):
    name = 'Ski_Boots'
    start_urls = ['https://www.evo.com/shop/ski/boots']

    item_measurement = ''

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
