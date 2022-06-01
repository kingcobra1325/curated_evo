from curated_evo.spider_templates import EvoSpider

class SkisSpider(EvoSpider):
    name = 'Skis'
    start_urls = ['https://www.evo.com/shop/ski/skis']

    item_measurement = 'cm'

    excluded_data = [
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
