from curated_evo.spider_templates import EvoSpider

class SkisSpider(EvoSpider):
    name = 'Skis'
    start_urls = ['https://www.evo.com/shop/ski/skis']

    item_measurement = 'cm'

    data_to_scrape = [
                        "Name",                                            
                        "Brand", 
                        "Image Source URLs",                                            
                        "Sale Price",
                        "Original Price",
                        "Available Colors",
                        "Available Sizes",
                        "Condition",
                        # ski / snowboard
                        "Terrain",
                        "Ability Level",
                        "Rocker Type",
                        # ski only
                        "Turning Radius",
                        "Waist Width",
                        # snowboard only
                        # "Flex Rating",
                        # "Shape",
                    ]
