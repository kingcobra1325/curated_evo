from curated_evo.spider_templates import EvoSpider

class SkiPolesSpider(EvoSpider):
    name = 'Ski_Poles'
    start_urls = ['https://www.evo.com/shop/ski/poles']

    item_measurement = 'in'

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
                        # "Terrain",
                        # "Ability Level",
                        # "Rocker Type",
                        # ski only
                        # "Turning Radius",
                        # "Waist Width",
                        # snowboard only
                        # "Flex Rating",
                        # "Shape",
                    ]
