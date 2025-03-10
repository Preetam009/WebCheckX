import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "scrapper"

SPIDER_MODULES = ["scrapper.spiders"]
NEWSPIDER_MODULE = "scrapper.spiders"

BASE_PATH = os.getenv('BASE_PATH')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
ENV_FILE = os.path.join(BASE_PATH, 'scrapper/scrapper/.env')
DATE_TODAY = date.today().strftime('%Y-%m-%d')

if not os.path.exists(os.path.join(OUTPUT_PATH, DATE_TODAY)):
    os.makedirs(os.path.join(OUTPUT_PATH, DATE_TODAY))
    
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(OUTPUT_PATH, DATE_TODAY, 'logs.txt')
LOG_FORMATE = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"    

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
DOWNLOAD_DELAY = 1

RETRY_ENABLED = True
RETRY_TIMES = 1
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 403]

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

TELNETCONSOLE_ENABLED = True

COOKIES_ENABLED = True
COOKIES_DEBUG = True

#SPIDER_MIDDLEWARES = {
#    "scrapper.middlewares.ScrapperSpiderMiddleware": 543,
#}

#DOWNLOADER_MIDDLEWARES = {
#    "scrapper.middlewares.ScrapperDownloaderMiddleware": 543,
#}

#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

#ITEM_PIPELINES = {
#    "scrapper.pipelines.ScrapperPipeline": 300,
#}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "slow_mo": 1000,
    "args": ['--disable-gpu', '--no-sandbox', '--log-level=3', '--allow-insecure-localhost', '--ignore-certificate-errors', '--ignore-ssl-errors'],
    "devtools": True,
    "timeout": 60000,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
