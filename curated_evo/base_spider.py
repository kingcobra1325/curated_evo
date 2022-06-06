from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader

import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException,NoSuchAttributeException

from scrapy_selenium import SeleniumRequest

from .dataframes import gsheet

class BaseSeleniumSpider(scrapy.Spider):
    name = 'DefaultSpiderName'
    allowed_domains = []
    start_urls = []
    item_data_label = []
    excluded_data = []

    meta_data = {}

    def exception_handler(self,error,response):
        gsheet.read_worksheet('ERRORS')
        error_data = {
                        "Time" : datetime.utcnow(),
                        'Spider' : self.name,
                        'Process' : "Spider Scraping",
                        "URL" : response.request.meta['driver'].current_url,
                        "Error" : f"{type(error).__name__}\n{error}",
                        "Traceback" : traceback.format_exc(),

                    }
        gsheet.add_row_to_sheet(error_data,'ERRORS')

    def start_requests(self):
        self.meta_data.update({
                    "spider_name":self.name,
                    "item_data_label":self.item_data_label,
                    "excluded_data":self.excluded_data,
                    })
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.initial_parse,
                meta=self.meta_data)
    
    def initial_parse(self, response):
        pass
    
    def scrape_xpath(self,driver,xpath_list=[],multi=False,wd_wait=0):
        for xpath in xpath_list:
            try:
                if multi:
                    result = WebDriverWait(driver,wd_wait).until(EC.presence_of_all_elements_located((By.XPATH, xpath))) if wd_wait else driver.find_elements_by_xpath(xpath)
                    if not result:
                        continue
                else:
                    result = WebDriverWait(driver,wd_wait).until(EC.presence_of_element_located((By.XPATH, xpath))) if wd_wait else driver.find_element_by_xpath(xpath)
                    result = result.get_attribute('textContent')
                return result
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"Xpath not found |{e}|")
        raise NoSuchElementException(f"No Valid XPATH:\n"+"\n".join(xpath_list))
    
    def copy_empty_results(self,item_data_label):
        empty_item_dict = {
                        "last_updated":"N/A",
                    }
        # Create Empty Dict from Data
        for item in item_data_label:
            empty_item_dict.update({item:"N/A"})
        return empty_item_dict
    
    def load_item_from_dict(self,item_data,item_class):
        data = ItemLoader(item = item_class())
        for item_key in list(item_data):
            data.add_value(item_key,item_data[item_key])
        return data.load_item()