#!/usr/bin/env python3

import dateparser
import math
from datetime import datetime, timedelta
from scrapy import Spider, Request
from w3lib.url import add_or_replace_parameters, url_query_parameter

class ShanghaiSpider(Spider):

    name = 'shanghai'
    allowed_domains = ['xyfw.fgw.sh.gov.cn']
    start_urls = [
        'https://xyfw.fgw.sh.gov.cn/credit-front/doublepublic/dictData?f=0&page=1&type=oc&p=&d=&title=',
        'https://xyfw.fgw.sh.gov.cn/credit-front/doublepublic/dictData?f=0&page=1&type=ox&p=&d=&title=',
    ]
    max_days = timedelta(days=7)
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 5,
        'TELNETCONSOLE_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.3.1.9 Safari/528.23',
    }

    def parse(self, response):
        if self.max_days <= timedelta(days=7):
            yield from self.parse_dept(response)
        else:
            for d in response.json()['depts']:
                url = add_or_replace_parameters(response.url, {'d': d})
                yield Request(url, callback=self.parse_dept)

    def parse_dept(self, response):
        data = response.json()
        _type = url_query_parameter(response.url, 'type')
        page = int(url_query_parameter(response.url, 'page'))
        for item in data['list']:
            item['_type'] = _type
            date = dateparser.parse(item.get('punishedAt') or item.get('billDate'))
            if datetime.now() - date < self.max_days:
                yield item
            else:
                break
        else:
            total = data['total']
            page_size = 20
            max_page = min(10, math.ceil(total/page_size))
            next_page = page + 1
            if next_page <= max_page:
                url = add_or_replace_parameters(response.url, {'page': next_page})
                yield Request(url, callback=self.parse_dept)

