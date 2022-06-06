from curated_evo.spider_templates import EvoSpider

class SnowboardJacketsSpider(EvoSpider):
    name = 'Snowboard_Jackets'
    start_urls = ['https://www.evo.com/shop/snowboard/jackets']

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
