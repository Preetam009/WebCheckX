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

    