from curated_evo.spider_templates import EvoSpider


class SnowboardsSpider(EvoSpider):
    name = 'Snowboards'
    start_urls = ['https://www.evo.com/shop/snowboard/snowboards']

    item_measurement = 'cm'

    excluded_data = [
                    "turning_radius",
                    "waist_width",
                    ]

    item_data_label = [
                    "name",                                            
                    "brand", 
                    "image_source_url",                                            
                    "sale_price",
                    "orig_price",
                    "available_colors",
                    "available_sizes",
                    "condition",
                    # ski / snowboard
                    "terrain",
                    "ability_level",
                    "rocker_type",
                    # ski only
                    "turning_radius",
                    "waist_width",
                    # snowboard onlys
                    "flex_rating",
                    "shape",
                    ]