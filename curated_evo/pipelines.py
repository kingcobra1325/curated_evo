# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from curated_evo.dataframes import gsheet

class WriteGoogleSheetsPipeline:

    sheetname = "CuratedEvo"

    def open_spider(self,spider):
        self.gsheet = gsheet
        self.gsheet.read_worksheet(name=self.sheetname)

    def process_item(self, item, spider):

        # SET ITEM ADAPTER
        adapter = ItemAdapter(item)

        data = {
                    "Last Updated": adapter.get("last_updated")[0],
                    "Type": adapter.get("type")[0],
                    "Name": adapter.get("name")[0],                                            
                    "URL": adapter.get("url")[0],
                    "Brand":adapter.get("brand")[0], 
                    "Image Source URLs": adapter.get("image_source_url")[0],                                            
                    "Sale Price": adapter.get("sale_price")[0],
                    "Original Price": adapter.get("orig_price")[0],
                    "Available Colors": adapter.get("available_colors")[0],
                    "Available Sizes": adapter.get("available_sizes")[0],
                    "Condition": adapter.get("condition")[0],
                    "Terrain": adapter.get("terrain")[0],
                    "Ability Level": adapter.get("ability_level")[0],
                    "Rocker Type": adapter.get("rocker_type")[0],
                    "Turning Radius": adapter.get("turning_radius")[0],
                    "Waist Width": adapter.get("waist_width")[0],
                    "Flex Rating": adapter.get("flex_rating")[0],
                    "Shape": adapter.get("shape")[0],
            }

        self.gsheet.add_data_row(data,self.sheetname)
        print(f"|{self.sheetname}| Row Count: {self.gsheet.dataframes[self.sheetname].shape[0]}")
        
        return item
    
    def close_spider(self,spider):
        # self.gsheet.write_worksheet(name=self.sheetname)
        pass

