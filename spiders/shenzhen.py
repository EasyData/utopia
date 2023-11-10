#!/usr/bin/env python3

import dateparser
import json
from datetime import datetime, timedelta
from scrapy import Spider
from scrapy.http import JsonRequest

class ShenzhenSpider(Spider):

    name = 'shenzhen'
    allowed_domains = ['www.szcredit.org.cn']
    start_urls = [
        'https://www.szcredit.org.cn/api/dmenterprise/permtipublicity',
        'https://www.szcredit.org.cn/api/dmenterprise/punishpublicity',
    ]
    max_days = timedelta(days=7)
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 5,
        'TELNETCONSOLE_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.3.1.9 Safari/528.23',
    }

    def parse(self, response):
        result = response.json()
        for item in result['Data']:
            yield item
