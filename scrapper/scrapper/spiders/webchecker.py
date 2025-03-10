import os
import re
import time
import scrapy
import xmlschema
import pandas as pd
from datetime import date
from dotenv import load_dotenv
from urllib.parse import urlparse, urljoin
from scrapy_playwright.page import PageMethod

load_dotenv()

BASE_PATH = os.getenv('BASE_PATH')
INPUT_PATH = os.path.join(BASE_PATH, 'input')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
SCHEMA_PATH = os.path.join(BASE_PATH, 'schema')
ENV_FILE = os.path.join(BASE_PATH, 'scrapper/scrapper/.env')
DATE_TODAY = date.today().strftime('%Y-%m-%d')

class WebcheckerSpider(scrapy.Spider):
    name = "webchecker"
    data = None
    path = os.getenv('INPUT_FILE')
    is_visited = set()
    ignore = ('#', 'tel:', 'mailto:', 'skype:', 'javascript:', 'callto:', 'fax:', 'SMS:', '.png', '.jpg', '.jpeg', '.svg', '.pdf', '.mp3', '.mp4', '.img', 'javascript:void(0)', 'void(0)', 'javascript', 'invoid(0)', 'Errors()')

    def __init__(self, *args, **kwargs):
        
        super(WebcheckerSpider, self).__init__(*args, **kwargs)
        
        FILE_PATH = os.path.join(INPUT_PATH, os.getenv('INPUT_FILE'))
        
        try:
            if FILE_PATH.endswith('.csv'):
                self.data = pd.read_csv(FILE_PATH)
                self.logger.info(f"CSV File loaded: {os.getenv('INPUT_FILE')}")
                
            elif FILE_PATH.endswith('.xlsx'):
                self.data = pd.read_excel(FILE_PATH)
                self.logger.info(f"CSV File loaded: {os.getenv('INPUT_FILE')}")
            
            self.data = self.data
            self.data.dropna(inplace=True)
            self.data.drop_duplicates(inplace=True)
            self.logger.info(f"Columns in File: {self.data.columns}")
            self.logger.info(f"Number of URLs: {self.data.shape[0]}")
            
        except Exception as e:
            self.logger.error(f"Error in reading file: {e}")
            
    def ensure_scheme(self, url, scheme):
        
        if isinstance(url, str) and url.strip():
            parsed_url = urlparse(url)
            
            if not(parsed_url.scheme):
                return scheme + url
            return url
        return None
    
    def start_requests(self):
        
        for data in self.data.itertuples(index=False, name=None):
            
            try:
                if not((data[0].endswith(self.ignore)) or (data[0].startswith(self.ignore)) or (data[0]==None)):
                    
                    scheme = 'http://'
                    normalized_url = self.ensure_scheme(data[0], scheme)
                    netloc = urlparse(normalized_url).netloc
                    sitemap_url = urljoin(normalized_url, 'sitemap.xml')
                    
                    try:
                        if normalized_url not in self.is_visited:
                            self.is_visited.add(normalized_url)
                            
                            yield scrapy.Request(
                                url=normalized_url,
                                callback=self.parse,
                                meta=dict(
                                    playwright=True,
                                    playwright_include_page=True,
                                    original_url=data[0],
                                    normalized_url=normalized_url,
                                    netloc=netloc,
                                    scheme=scheme,
                                ),
                                dont_filter=True,
                                errback=self.inactive,
                            )
                        
                    except Exception as e:
                        self.logger.error(f"Error in start_requests for {normalized_url}: {e}")
                    
            except Exception as e:
                self.logger.error(f"Error in start_requests for {data[0]: {e}}")
                continue
            
    def parse(self, response):
        print(response)
        
    def inactive(self, failure):
        
        scheme = failure.request.meta.get('scheme', None)
        url = failure.request.meta.get('original_url', None)
        
        if scheme=='http://':
            try:
                normalized_url = self.ensure_scheme(url, 'https://')
                netloc = urlparse(normalized_url).netloc
                
                if normalized_url not in self.is_visited:
                    self.is_visited.add(normalized_url)
                    
                    yield scrapy.Request(
                        url=normalized_url,
                        callback=self.parse,
                        meta=dict(
                            playwright=True,
                            playwright_include_page=True,
                            original_url=url,
                            normalized_url=normalized_url,
                            netloc=netloc,
                            scheme='https://',
                            ),
                        dont_filter=True,
                        errback=self.inactive,
                    )
                
            except Exception as e:
                self.logger.error(f"Error in inactive for {url}: {e}")
                
        elif scheme=='https://':
            print(url)