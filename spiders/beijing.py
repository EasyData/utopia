#!/usr/bin/env python3

import dateparser
import json
from datetime import datetime, timedelta
from scrapy import Spider
from scrapy.http import JsonRequest

class BeijingSpider(Spider):

    name = 'beijing'
    allowed_domains = ['creditbj.jxj.beijing.gov.cn']
    start_urls = [
        'https://creditbj.jxj.beijing.gov.cn/credit-portal/api/publicity/record/ALLOW/0',
        'https://creditbj.jxj.beijing.gov.cn/credit-portal/api/publicity/record/PUNISH/0',
    ]
    max_days = timedelta(days=7)
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 5,
        'TELNETCONSOLE_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.3.1.9 Safari/528.23',
    }

    def start_requests(self):
        for url in self.start_urls:
            data = {
                "listSql": "",
                "linesPerPage": 10,
                "currentPage": 1,
                "condition": {
                    "keyWord": "",
                }
            }
            if 'ALLOW' in url:
                data['condition']['creditObjectType'] = '0'
                referer = 'https://creditbj.jxj.beijing.gov.cn/credit-portal/publicity/record/allow_publicity'
            else:
                data['condition']['openStyle'] = '2'
                referer = 'https://creditbj.jxj.beijing.gov.cn/credit-portal/publicity/record/punish_publicity'
            yield JsonRequest(url, data=data, headers={'Referer': referer})

    def parse(self, response):
        url = response.url
        result = response.json()
        for item in result['data']['list']:
            date = dateparser.parse(item['zhgxsj'])
            if datetime.now() - date < self.max_days:
                yield item
            else:
                break
        else:
            page = result['data']['page']['currentPage']
            max_page = min(5, result['data']['page']['totalPage'])
            next_page = page + 1
            if next_page <= max_page:
                data = json.loads(response.request.body.decode('utf-8'))
                referer = response.request.headers['Referer']
                data['currentPage'] = next_page
                yield JsonRequest(url, data=data, headers={'Referer': referer})

