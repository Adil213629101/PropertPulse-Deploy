import json
import math

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent

from utils.utils import append_list_to_json_file, extract_property_details, save_list_to_json

ua = UserAgent


class RealtorScraper:

    def __init__(self, url,filepath):
        self.url = url
        self.filepath=filepath
        self.pageProps = None
        self.totalProperties = 0
        self.fetchProperties = 0
        self.resultProperties = []
        self.page_size = 42
        self.page = 1
        self.endpage = 1

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

    def make_request(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
        except requests.ConnectionError:
            print("Connection error")
        except Exception as e:
            print(e.__class__)

    def parse_page(self, response):
        if response is not None:
            soup = BeautifulSoup(response.content, "html.parser")
            next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
            if next_data_script:
                content = json.loads(next_data_script.string)
                props = content["props"]
                self.pageProps = props["pageProps"]
                properties = self.pageProps['properties']
                return properties
            else:
                print("captcha Found")
                return None

    def parse_properties(self, properties):
        processed_properties = []
        for property in properties:
            try:
                processed = extract_property_details(property)
                processed_properties.append(processed)
            except Exception as e:
                print(f"Cannot extract details")
                raise e
        return processed_properties

    def meta_data(self):
        meta_data = {}
        try:
            meta_data['totalProperties'] = self.pageProps.get('totalProperties')
            meta_data['city'] = self.pageProps["geo"].get("city")
            meta_data['state_code'] = self.pageProps["geo"].get("state_code")
            meta_data['country'] = self.pageProps["geo"].get("country")
            meta_data['slug_id'] = self.pageProps["geo"].get("slug_id")
            return meta_data
        except KeyError:
            print("Meta Deta Error")
            raise KeyError("URL not found")
    def initialize(self):
        res = self.make_request(self.url)
        try:
            properties = self.parse_page(res)
            self.page_data = self.meta_data()

            self.totalProperties = self.page_data.get("totalProperties")
            self.endpage = math.ceil(self.totalProperties/self.page_size)

            processed_properties = self.parse_properties(properties)
            self.resultProperties+=(processed_properties)
            self.fetchProperties += len(processed_properties)
        except Exception as e:
            raise KeyError("Invalid URL")

    def scrape(self):
        try:
            for i in range(2, self.endpage+1):
                url = f'{self.url}pg-{i}'
                print(f"scraping  : {url}")
                response = self.make_request(url)
                properties = self.parse_page(response)
                if properties is not None:
                    print(f"scraped page : {i} : {len(properties)}")
                    processed_properties = self.parse_properties(properties)
                    self.resultProperties+=processed_properties
                    append_list_to_json_file(
                        data_list=properties, filename=self.filepath)
                    self.fetchProperties += len(processed_properties)
        except Exception as e:
            print(e.__class__)
            print(url)
            raise e
        return self.resultProperties,self.meta_data()


if __name__ == '__main__':
    url='https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA/type-single-family-home/price-na-600000/'
    scraper = RealtorScraper(url,filepath="../dc.json")
    scraper.initialize()
    result = scraper.scrape()
    print(len(result[0]))
    # save_list_to_json(data_list=result[0], filename="test.json")
