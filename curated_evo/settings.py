import ast
from os import environ
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv('.env')

# Scrapy settings for curated_evo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'curated_evo'

SPIDER_MODULES = ['curated_evo.spiders']
NEWSPIDER_MODULE = 'curated_evo.spiders'


# BASE SETTINGS
PRODUCTION = False
SERVICE_EMAIL = environ['SERVICE_EMAIL']
SPREADSHEET_ID = environ['SPREADSHEET_ID']
GOOGLE_API_KEY = ast.literal_eval(environ['GOOGLE_SERVICE_ACCOUNT'])

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'curated_evo (+http://www.yourdomain.com)'
USER_AGENT_LIST = [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",

                    ]

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'curated_evo.middlewares.CuratedEvoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'curated_evo.middlewares.RotateUserAgentMiddleware': 100,
   'scrapy_selenium.SeleniumMiddleware': 200,
}

# GSHEET SETTINGS

GSHEET_NAME = "CuratedEvo"
GSHEET_COLUMNS = [
                        "Last Updated",
                        "Type",
                        "Name",
                        "URL",                                            
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
                        "Flex Rating",
                        "Shape",
                     ]

# PANDAS SETTINGS
SAVE_TO_DATAFRAME = False

# SELENIUM SETTINGS
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = "/home/linux2/codes/webdrivers/chromedriver"
SELENIUM_DRIVER_ARGUMENTS=['--headless']

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}pip install git+https://github.com/dylanwalker/better-scrapy-selenium.git

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'curated_evo.pipelines.WriteGoogleSheetsPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
