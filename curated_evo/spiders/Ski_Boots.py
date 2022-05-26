from curated_evo.spider_templates import EvoSpider

class SkiBootsSpider(EvoSpider):
    name = 'Ski_Boots'
    start_urls = ['https://www.evo.com/shop/ski/boots']

    item_measurement = ''

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
