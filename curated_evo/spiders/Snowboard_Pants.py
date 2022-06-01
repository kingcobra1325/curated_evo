from curated_evo.spider_templates import EvoSpider

class SnowboardPantsSpider(EvoSpider):
    name = 'Snowboard_Pants'
    start_urls = ['https://www.evo.com/shop/snowboard/pants']

    item_measurement = ''

    excluded_data = [
                    "terrain",
                    "ability_level",
                    "rocker_type",
                    "turning_radius",
                    "waist_width",
                    "flex_rating",
                    "shape",
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
