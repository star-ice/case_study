import scrapy
import openpyxl as opxl
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy.http import FormRequest
import json
import case_crawler.settings as settings
import os

class CaseSpider(scrapy.Spider):
    name = "lawsdataLogin"
    allowed_domains = ["lawsdata.com"]
    start_urls = "https://www.lawsdata.com/api/compass-auth/login/account"
    test_url_1 = 'https://www.lawsdata.com/api/compass-front/detail/getInstrumentById/57aa182ac2265c28a55226ac'
    test_url_2 = 'https://www.lawsdata.com/#/documentDetails?id=57aa182ac2265c28a55226ac&type=1'

    def start_requests(self):
        # url = "http://www.myntra.com/search-service/searchservice/search/filteredSearch"
        payload = {"account":"13934788837","password":"5598EF126B92325396B4F9062236F1AE"}
        yield FormRequest(self.start_urls, self.after_login, method="POST", body=json.dumps(payload))


    # def parse(self, response):
    #     # print(response.text)
    #     # yield Request(self.test_url, self.parse_test)
    #     payload = {"account": "13934788837", "password": "5598EF126B92325396B4F9062236F1AE"}
    #     return [FormRequest.from_response(response,
    #                                       formdata=json.dumps(payload),
    #                                       callback=self.after_login)]

    def after_login(self, response):
        res_json = eval(response.text)
        print(res_json)
        headers = settings.DEFAULT_REQUEST_HEADERS
        headers['authentication'] = res_json['returnData']
        print(headers)
        yield Request(self.test_url_1, self.parse_test, headers=headers)

    def parse_test(self, response):
        print(response.text)
        print()

