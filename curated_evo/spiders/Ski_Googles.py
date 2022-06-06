from curated_evo.spider_templates import EvoSpider


class SkiGooglesSpider(EvoSpider):
    name = 'Ski_Googles'
    start_urls = ['https://www.evo.com/shop/ski/ski-goggles']

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