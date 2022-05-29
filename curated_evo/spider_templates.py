from datetime import datetime
from re import T

import scrapy
import traceback

from scrapy.loader import ItemLoader

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException,NoSuchAttributeException

from scrapy_selenium import SeleniumRequest

from .decorators import decorate
from .dataframes import gsheet
from .items import CuratedEvoItem

# BASE CLASS SPIDERS #

class BaseSeleniumSpider(scrapy.Spider):
    name = 'DefaultSpiderName'
    allowed_domains = []
    start_urls = []
    data_to_scrape = []
    item_urls=[]

    meta_data = {}

    def exception_handler(self,error,driver):
        error_data = {
                        "Time" : datetime.utcnow(),
                        'Spider' : self.name,
                        'Process' : "Spider Scraping",
                        "URL" : driver.current_url,
                        "Error" : f"{type(error).__name__}\n{error}",
                        "Traceback" : traceback.format_exc(),

                    }
        gsheet.add_row_to_sheet(error_data,'ERRORS')

    @decorate.selenium_spider_exception()
    def start_requests(self):
        self.meta_data.update({
                    "spider_name":self.name,
                    "data_to_scrape":self.data_to_scrape,
                    })
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.initial_parse,
                meta=self.meta_data)
    
    def initial_parse(self, response):
        pass
    
    def scrape_xpath(self,driver,xpath_list=[],multi=False):
        for xpath in xpath_list:
            try:
                if multi:
                    result = driver.find_elements_by_xpath(xpath)
                    if not result:
                        continue
                else:
                    result = driver.find_element_by_xpath(xpath).get_attribute('textContent')
                return result
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"Xpath not found |{e}|")
        raise NoSuchElementException(f"No Valid XPATH:\n"+"\n".join(xpath_list))

# SPIDERS #

class EvoSpider(BaseSeleniumSpider):
    allowed_domains = ['www.evo.com']

    item_measurement = ''

    def start_requests(self):
        self.meta_data.update({
            "item_measurement":self.item_measurement
            })
        return super().start_requests()

    @decorate.selenium_spider_exception()
    def initial_parse(self, response):
        driver = response.request.meta['driver']
        spider_name = response.request.meta['spider_name']
        data_to_scrape = response.request.meta['data_to_scrape']
        item_measurement = response.request.meta['item_measurement']

        item_urls = []
        next_page_raw = driver.find_element(By.XPATH,"//a[contains(@class,'results-next')]").get_attribute('href')
        raw_link = next_page_raw.replace("#","").split("/")
        only_href = next_page_raw.replace(driver.current_url,"").replace("#","")
        base_url = "/".join(raw_link[0:(raw_link.index(self.allowed_domains[0])+1)])
        next_page = base_url+only_href
        self.logger.debug(f"THIS IS THE LINK = {next_page}")
        next_page_template = next_page.split("/")
        for page in range(2,100000):
            try:
                raw_items_list = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='product-thumb-details']//a")))
                items_list = [x.get_attribute('href') for x in raw_items_list]
                item_urls.extend(items_list)
                self.logger.debug(f"Number of Items: {len(items_list)} - Total: {len(item_urls)} - Uniques: {len(list(set(item_urls)))}")
            except(NoSuchElementException,TimeoutException,StaleElementReferenceException) as e:
                self.logger.debug(f"No more pages to crawl |{e}|")
                break
            page_template = next_page_template.copy()
            page_template[-1] = f'p_{page}'
            next_page = "/".join(page_template)
            self.logger.debug(f"Next Page Link -> {next_page}")
            driver.get(next_page)
        self.logger.debug(f"Total Number of Items to scrape: {len(item_urls)}")
        for item in item_urls:
            self.logger.debug(f"Item Link: {item}")
            yield SeleniumRequest(url=item,
                callback=self.parse_item,
                meta={
                'spider_name':spider_name,
                "data_to_scrape":data_to_scrape,
                "item_measurement":item_measurement,
                "item_urls":item_urls,
                })

    @decorate.selenium_spider_exception()
    def parse_item(self,response):
        driver = response.request.meta['driver']
        data_to_scrape = response.request.meta['data_to_scrape']
        item_measurement = response.request.meta['item_measurement']
        result = self.copy_empty_results()
        result["Type"] = response.request.meta['spider_name'].replace("_"," ")
        result['URL'] = response.url
        driver.get(result['URL'])
        if 'Name' in data_to_scrape:
            name = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='pdp-header-title']"))).get_attribute('textContent')
            result['Name'] = name
        if 'Brand' in data_to_scrape:
            raw_data = driver.find_element_by_xpath("//div[@class='pdp-description-brand']/a").get_attribute('href')
            brand = raw_data.split('/')[-1]
            result['Brand'] = brand
        if 'Image Source URLs' in data_to_scrape:
            raw_images = driver.find_elements_by_xpath("//div[contains(@class,'js-pdp-hero-container')]//img")
            img_src_raw = list(set([f"{x.get_attribute('src')}" for x in raw_images if 'data:image' not in x.get_attribute('src')]))
            image_src_list = "\n".join(img_src_raw)
            result['Image Source URLs'] = image_src_list
        if "Sale Price" in data_to_scrape:
            try:
                price_sale = driver.find_element_by_xpath("//span[contains(@class,'pdp-price-discount')]").get_attribute('textContent')
                result["Sale Price"] = price_sale
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"No sale price found |{e}|")
                check_sales_text = driver.find_element_by_xpath("//div[@id='buy-grid']").get_attribute('textContent').lower()
                if 'sale' in check_sales_text:
                    self.exception_handler(e,driver)
        if "Original Price" in data_to_scrape:
            result["Original Price"] = self.scrape_xpath(driver,xpath_list=[
                                                        "//span[contains(@class,'pdp-price-message')]",
                                                        "//span[contains(@class,'pdp-price-regular') and contains(@class,'no-wrap')]",
                                                        "//span[contains(@class,'pdp-price-regular')]"])
        if "Available Colors" in data_to_scrape:
            try:
                raw_colors = self.scrape_xpath(driver,xpath_list=[
                                                                "//div[contains(text(),'Please select') and contains(text(),'color')]/following-sibling::ul//img",
                                                                "//div[contains(text(),'Please select') and contains(text(),'color')]/following-sibling::ul//span",
                                                                "//div[text()='Please select a color']/following-sibling::ul//img",
                                                                "//div[text()='Please select a color']/following-sibling::ul//span",
                                                                ],multi=True)
                avail_colors = "\n".join([f"{x.get_attribute('alt')}" for x in raw_colors])
                result["Available Colors"] = avail_colors
            except NoSuchAttributeException as e:
                avail_colors = "\n".join([x.get_attribute('title').split(" ")[-1] for x in raw_colors])
                result["Available Colors"] = avail_colors
            except NoSuchElementException as e:
                self.logger.debug(f"No available colors found |{e}|")
                # check_colors_text = driver.find_element_by_xpath("//div[@id='buy-grid']").get_attribute('textContent').lower()
                # if 'color' in check_colors_text:
                    # self.exception_handler(e,driver)
        if "Available Sizes" in data_to_scrape:
            try:
                raw_sizes = self.scrape_xpath(driver,[
                    "//div[text()='Please select a size']/following-sibling::ul//span[contains(@class,'pdp-selection-text')]",
                    "//div[contains(text(),'Please select') and contains(text(),'size')]/following-sibling::ul//span[contains(@class,'pdp-selection-text')]",                        
                ],multi=True)
                avail_sizes = "\n".join([f"{x.get_attribute('textContent')}{item_measurement}".replace("\n","") for x in raw_sizes])
                result["Available Sizes"] = avail_sizes
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"No available sizes found |{e}|")
                check_size_text = driver.find_element_by_xpath("//div[@id='buy-grid']").get_attribute('textContent').lower()
                if 'size' in check_size_text:
                    self.exception_handler(e,driver)
        if "Condition" in data_to_scrape:
            if 'used' in result["Name"].lower():
                condition_status = "Used"
            else:
                condition_status = "New"
            try:
                raw_condition = self.scrape_xpath(driver,[
                    "//div[contains(text(),'Please select a condition')]/following-sibling::ul//span[contains(@class,'pdp-selector')]",
                    ],multi=True)
                condition = f"{condition_status}\n"+"\n".join([f"{x.get_attribute('textContent')}" for x in raw_condition])
                result.update({"Condition":condition})
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"No available conditions found |{e}|")
                if 'used' in result["Name"].lower():
                    self.exception_handler(e,driver)
                result.update({"Condition":condition_status})
        if "Terrain" in data_to_scrape:
            try:
                terrain = driver.find_element_by_xpath("//li[contains(@class,'spec-terrain')]/span[@class='pdp-spec-list-description']").get_attribute('textContent')
                result["Terrain"] = terrain
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No terrain found |{e}|")
                self.exception_handler(e,driver)
        if "Ability Level" in data_to_scrape:
            try:
                ability_lvl = driver.find_element_by_xpath("//li[contains(@class,'ability')]/span[@class='pdp-spec-list-description']").get_attribute('textContent')
                result["Ability Level"] = ability_lvl
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No ability level found |{e}|")
                self.exception_handler(e,driver)
        if "Rocker Type" in data_to_scrape:
            try:
                rocker_type = self.scrape_xpath(driver,[
                                                    "//h5[text()='Rocker Type']/following-sibling::div[@class='pdp-feature-description']",
                                                    "//strong[contains(text(),'Rocker Type')]/parent::span/following-sibling::span"
                                                    ])
                result["Rocker Type"] = rocker_type
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No rocker type found |{e}|")
                self.exception_handler(e,driver)
        if "Turning Radius" in data_to_scrape:
            try:
                turning_radius = self.scrape_xpath(driver,[
                                                    "//li[contains(@class,'turning-radius')]/span[@class='pdp-spec-list-description']",
                                                    "//th[contains(text(),'Turning Radius')]/parent::tr",
                                                    ]).replace("Turning Radius","")
                result["Turning Radius"] = turning_radius
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No turning radius found |{e}|")
                self.exception_handler(e,driver)
        if "Waist Width" in data_to_scrape:
            try:
                raw_waist_width = driver.find_elements_by_xpath("//th[contains(text(),'Waist Width')]/following-sibling::td")
                waist_width = "\n".join([f"{x.get_attribute('textContent')}mm" for x in raw_waist_width if x.get_attribute('textContent')])
                result["Waist Width"] = waist_width
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No waist width found |{e}|")
                self.exception_handler(e,driver)
        if "Flex Rating" in data_to_scrape:
            try:
                flex_rating = self.scrape_xpath(driver,[
                    "//h5[text()='Flex']/following-sibling::div[@class='pdp-feature-description']",
                    "//li[contains(@class,'spec-flex-rating')]//span[contains(@class,'pdp-spec-list-description')]",
                ])
                result["Flex Rating"] = flex_rating
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No flex rating found |{e}|")
                self.exception_handler(e,driver)
        if "Shape" in data_to_scrape:
            try:
                shape = self.scrape_xpath(driver,[
                    "//h5[text()='Shape']/following-sibling::div[@class='pdp-feature-description']",
                    "//li[contains(@class,'spec-shape')]//span[contains(@class,'pdp-spec-list-description')]",
                ])
                result["Shape"] = shape
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No shape found |{e}|")
                self.exception_handler(e,driver)        
        result["Last Updated"] = datetime.utcnow()
        self.logger.debug(result)
        
        yield self.load_item_from_dict(result)
    
    def copy_empty_results(self):
        return {
                    "Type" : "N/A",
                    "Last Updated":"N/A",
                    "URL":"N/A",
                    "Name":"N/A",                                            
                    "Brand":"N/A", 
                    "Image Source URLs":"N/A",                                            
                    "Sale Price":"N/A",
                    "Original Price":"N/A",
                    "Available Colors":"N/A",
                    "Available Sizes":"N/A",
                    "Condition":"N/A",
                    "Terrain":"N/A",
                    "Ability Level":"N/A",
                    "Rocker Type":"N/A",
                    "Turning Radius":"N/A",
                    "Waist Width":"N/A",
                    "Flex Rating":"N/A",
                    "Shape":"N/A",

        }
    
    def load_item_from_dict(self,item_data):

        data = ItemLoader(item = CuratedEvoItem())
        data.add_value('last_updated', item_data["Last Updated"])
        data.add_value('type',item_data["Type"])
        data.add_value('name',item_data['Name'])
        data.add_value('url', item_data['URL'])
        data.add_value('brand', item_data['Brand'])
        data.add_value('image_source_url', item_data['Image Source URLs'])
        data.add_value('sale_price', item_data['Sale Price'])
        data.add_value('orig_price', item_data['Original Price'])
        data.add_value('available_colors', item_data['Available Colors'])
        data.add_value('available_sizes', item_data['Available Sizes'])
        data.add_value('condition', item_data['Condition'])
        data.add_value('terrain', item_data['Terrain'])
        data.add_value('ability_level', item_data['Ability Level'])
        data.add_value('rocker_type', item_data['Rocker Type'])
        data.add_value('turning_radius', item_data['Turning Radius'])
        data.add_value('waist_width', item_data['Waist Width'])
        data.add_value('flex_rating', item_data['Flex Rating'])
        data.add_value('shape', item_data['Shape'])

        return data.load_item()