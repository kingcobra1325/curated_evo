from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException,NoSuchAttributeException

from scrapy_selenium import SeleniumRequest

from .items import CuratedEvoItem
from .decorators import decorate

# BASE SPIDER CLASS #

from .base_spider import BaseSeleniumSpider

# SPIDERS #

class EvoSpider(BaseSeleniumSpider):
    allowed_domains = ['www.evo.com']

    item_measurement = ''

    def start_requests(self):
        self.meta_data.update({
            "item_measurement":self.item_measurement
            })
        return super().start_requests()
    
    def copy_empty_results(self, item_data_label):
        item_data_label.extend(["type","url"])
        return super().copy_empty_results(item_data_label)

    @decorate.selenium_spider_exception()
    def initial_parse(self, response):
        driver = response.request.meta['driver']
        item_urls = []
        next_page_raw = driver.find_element(By.XPATH,"//a[contains(@class,'results-next')]").get_attribute('href')
        raw_link = next_page_raw.replace("#","").split("/")
        only_href = next_page_raw.replace(driver.current_url,"").replace("#","")
        base_url = "/".join(raw_link[0:(raw_link.index(self.allowed_domains[0])+1)])
        next_page = base_url+only_href
        self.logger.debug(f"THIS IS THE LINK = {next_page}")
        next_page_template = next_page.split("/")
        page=2
        while True:
            try:
                raw_items_list = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='product-thumb-details']//a")))
                items_list = [x.get_attribute('href') for x in raw_items_list]
                item_urls.extend(items_list)
                self.logger.debug(f"Number of Items: {len(items_list)} - Total: {len(item_urls)} - Uniques: {len(list(set(item_urls)))}")
                for item in items_list:
                    self.logger.debug(f"Item Link: {item}")
                    yield SeleniumRequest(url=item,
                        callback=self.parse_item,
                        meta=response.request.meta)
            except(NoSuchElementException,TimeoutException,StaleElementReferenceException) as e:
                self.logger.debug(f"No more pages to crawl |{e}|")
                break
            page_template = next_page_template.copy()
            page_template[-1] = f'p_{page}'
            next_page = "/".join(page_template)
            self.logger.debug(f"Next Page Link -> {next_page}")
            driver.get(next_page)
            page+=1

    @decorate.selenium_spider_exception()
    def parse_item(self,response):
        driver = response.request.meta['driver']
        item_data_label = response.request.meta['item_data_label']
        item_measurement = response.request.meta['item_measurement']
        excluded_data = response.request.meta['excluded_data']
        result = self.copy_empty_results(item_data_label)
        result["type"] = response.request.meta['spider_name'].replace("_"," ")
        result['url'] = response.url
        driver.get(result['url'])
        if 'name' not in excluded_data:
            name = self.scrape_xpath(driver,["//h1[@class='pdp-header-title']"],wd_wait=20)
            result['name'] = name
        if 'brand' not in excluded_data:
            raw_data = driver.find_element_by_xpath("//div[@class='pdp-description-brand']/a").get_attribute('href')
            brand = raw_data.split('/')[-1]
            result['brand'] = brand
        if 'image_source_url' not in excluded_data:
            raw_images = driver.find_elements_by_xpath("//div[contains(@class,'js-pdp-hero-container')]//img")
            img_src_raw = list(set([f"{x.get_attribute('src')}" for x in raw_images if 'data:image' not in x.get_attribute('src')]))
            image_src_list = "\n".join(img_src_raw)
            result['image_source_url'] = image_src_list
        if "sale_price" not in excluded_data:
            try:
                price_sale = driver.find_element_by_xpath("//span[contains(@class,'pdp-price-discount')]").get_attribute('textContent')
                result["sale_price"] = price_sale
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"No sale price found |{e}|")
                check_sales_text = driver.find_element_by_xpath("//div[@id='buy-grid']").get_attribute('textContent').lower()
                if 'sale' in check_sales_text:
                    self.exception_handler(e,response)
        if "orig_price" not in excluded_data:
            result["orig_price"] = self.scrape_xpath(driver,xpath_list=[
                                                        "//span[contains(@class,'pdp-price-message')]",
                                                        "//span[contains(@class,'pdp-price-regular') and contains(@class,'no-wrap')]",
                                                        "//span[contains(@class,'pdp-price-regular')]"])
        if "available_colors" not in excluded_data:
            try:
                raw_colors = self.scrape_xpath(driver,xpath_list=[
                                                                "//div[contains(text(),'Please select') and contains(text(),'color')]/following-sibling::ul//img",
                                                                "//div[contains(text(),'Please select') and contains(text(),'color')]/following-sibling::ul//span",
                                                                "//div[text()='Please select a color']/following-sibling::ul//img",
                                                                "//div[text()='Please select a color']/following-sibling::ul//span",
                                                                ],multi=True)
                avail_colors = "\n".join([f"{x.get_attribute('alt')}" for x in raw_colors])
                result["available_colors"] = avail_colors
            except NoSuchAttributeException as e:
                avail_colors = "\n".join([x.get_attribute('title').split(" ")[-1] for x in raw_colors])
                result["available_colors"] = avail_colors
            except NoSuchElementException as e:
                self.logger.debug(f"No available colors found |{e}|")
                # check_colors_text = driver.find_element_by_xpath("//div[@id='buy-grid']").get_attribute('textContent').lower()
                # if 'color' in check_colors_text:
                    # self.exception_handler(e,response)
        if "available_sizes" not in excluded_data:
            try:
                raw_sizes = self.scrape_xpath(driver,[
                    "//div[text()='Please select a size']/following-sibling::ul//span[contains(@class,'pdp-selection-text')]",
                    "//div[contains(text(),'Please select') and contains(text(),'size')]/following-sibling::ul//span[contains(@class,'pdp-selection-text')]",                        
                ],multi=True)
                avail_sizes = "\n".join([f"{x.get_attribute('textContent')}{item_measurement}".replace("\n","") for x in raw_sizes])
                result["available_sizes"] = avail_sizes
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"No available sizes found |{e}|")
                check_size_text = driver.find_element_by_xpath("//div[@id='buy-grid']").get_attribute('textContent').lower()
                if 'size' in check_size_text:
                    self.exception_handler(e,response)
        if "condition" not in excluded_data:
            if 'used' in result["name"].lower():
                condition_status = "Used"
            else:
                condition_status = "New"
            try:
                raw_condition = self.scrape_xpath(driver,[
                    "//div[contains(text(),'Please select a condition')]/following-sibling::ul//span[contains(@class,'pdp-selector')]",
                    ],multi=True)
                condition = f"{condition_status}\n"+"\n".join([f"{x.get_attribute('textContent')}" for x in raw_condition])
                result.update({"condition":condition})
            except (NoSuchElementException,TimeoutException) as e:
                self.logger.debug(f"No available conditions found |{e}|")
                if 'used' in result["name"].lower():
                    self.exception_handler(e,response)
                result.update({"condition":condition_status})
        if "terrain" not in excluded_data:
            try:
                terrain = driver.find_element_by_xpath("//li[contains(@class,'spec-terrain')]/span[@class='pdp-spec-list-description']").get_attribute('textContent')
                result["terrain"] = terrain
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No terrain found |{e}|")
                self.exception_handler(e,response)
        if "ability_level" not in excluded_data:
            try:
                ability_lvl = driver.find_element_by_xpath("//li[contains(@class,'ability')]/span[@class='pdp-spec-list-description']").get_attribute('textContent')
                result["ability_level"] = ability_lvl
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No ability level found |{e}|")
                self.exception_handler(e,response)
        if "rocker_type" not in excluded_data:
            try:
                rocker_type = self.scrape_xpath(driver,[
                                                    "//h5[text()='Rocker Type']/following-sibling::div[@class='pdp-feature-description']",
                                                    "//strong[contains(text(),'Rocker Type')]/parent::span/following-sibling::span"
                                                    ])
                result["rocker_type"] = rocker_type
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No rocker type found |{e}|")
                self.exception_handler(e,response)
        if "turning_radius" not in excluded_data:
            try:
                turning_radius = self.scrape_xpath(driver,[
                                                    "//li[contains(@class,'turning-radius')]/span[@class='pdp-spec-list-description']",
                                                    "//th[contains(text(),'Turning Radius')]/parent::tr",
                                                    ]).replace("Turning Radius","")
                result["turning_radius"] = turning_radius
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No turning radius found |{e}|")
                self.exception_handler(e,response)
        if "waist_width" not in excluded_data:
            try:
                raw_waist_width = driver.find_elements_by_xpath("//th[contains(text(),'Waist Width')]/following-sibling::td")
                waist_width = "\n".join([f"{x.get_attribute('textContent')}mm" for x in raw_waist_width if x.get_attribute('textContent')])
                result["waist_width"] = waist_width
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No waist width found |{e}|")
                self.exception_handler(e,response)
        if "flex_rating" not in excluded_data:
            try:
                flex_rating = self.scrape_xpath(driver,[
                    "//h5[text()='Flex']/following-sibling::div[@class='pdp-feature-description']",
                    "//li[contains(@class,'spec-flex-rating')]//span[contains(@class,'pdp-spec-list-description')]",
                ])
                result["flex_rating"] = flex_rating
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No flex rating found |{e}|")
                self.exception_handler(e,response)
        if "shape" not in excluded_data:
            try:
                shape = self.scrape_xpath(driver,[
                    "//h5[text()='Shape']/following-sibling::div[@class='pdp-feature-description']",
                    "//li[contains(@class,'spec-shape')]//span[contains(@class,'pdp-spec-list-description')]",
                ])
                result["shape"] = shape
            except (TimeoutException,NoSuchElementException) as e:
                self.logger.debug(f"No shape found |{e}|")
                self.exception_handler(e,response)        
        result["last_updated"] = datetime.utcnow()
        self.logger.debug(result)
        
        yield self.load_item_from_dict(result,CuratedEvoItem)