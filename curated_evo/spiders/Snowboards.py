from curated_evo.spider_templates import EvoSpider


class SnowboardsSpider(EvoSpider):
    name = 'Snowboards'
    start_urls = ['https://www.evo.com/shop/snowboard/snowboards']

    item_measurement = 'cm'

    excluded_data = [
                    # ski / snowboard
                    # "terrain",
                    # "ability_level",
                    # "rocker_type",
                    # ski only
                    "turning_radius",
                    "waist_width",
                    # snowboard only
                    # "flex_rating",
                    # "shape",
                    ]