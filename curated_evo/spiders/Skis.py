from curated_evo.spider_templates import EvoSpider

class SkisSpider(EvoSpider):
    name = 'Skis'
    start_urls = ['https://www.evo.com/shop/ski/skis']

    item_measurement = 'cm'

    excluded_data = [
                    # ski / snowboard
                    # "terrain",
                    # "ability_level",
                    # "rocker_type",
                    # ski only
                    # "turning_radius",
                    # "waist_width",
                    # snowboard only
                    "flex_rating",
                    "shape",
                    ]
