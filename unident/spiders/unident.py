import scrapy
from unident.items import UnidentItem
from bs4 import BeautifulSoup
import re
import os.path, sys
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
from config import Config



class UnidentshopSpider(scrapy.Spider):

    name = Config.name_parser
    start_urls = [Config.section_for_parsing]


    def __init__(self):
        self.declare_xpath()


    def declare_xpath(self):
        self.getAllProductsXpath = '//a[@class="product photo product-item-photo"]/@href'
        self.TitleXpath  = "//h1[@class='page-title']/text()"
        self.CodeProductXpath = '//div[@style="display:flex;justify-content: space-between;"]/div/p'
        self.CodeProducerXpath = '//div[@style="display:flex;justify-content: space-between;"]/div/p'
        self.priceXpath = '//span[@class="price"]'
        self.BrandXpath = '//a[@class="title_brand_url"]//text()'
        self.DescriptionXpath = '//div[@class="value"]/text()'


    def parse(self, response):
        for href in response.xpath(self.getAllProductsXpath):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_main_item)

        next_page_url = response.xpath("(//a[@class='action  next']/@href)[1]").extract()[0]
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url, callback=self.parse)


    def parse_main_item(self,response):
        print(123)
        item = UnidentItem()

        Title = response.xpath(self.TitleXpath).extract()[0].strip()
        Price = response.xpath(self.priceXpath).extract()[0]
        Price = self.parseText(Price)
        Brand = response.xpath(self.BrandXpath).extract()[0].strip()
        CodeProduct = response.xpath(self.CodeProductXpath).extract()[0]
        CodeProduct = self.parseText(CodeProduct).replace('Кодтоваа:', '').strip()
        CodeProducer = response.xpath(self.CodeProducerXpath).extract()[1]
        CodeProducer = self.parseText(CodeProducer).replace('Кодпоизводителя:', '').strip()
        Description = response.xpath(self.DescriptionXpath).extract()[1]


        item['Title']          = Title
        item['Price']          = Price
        item['Brand']          = Brand
        item['CodeProduct']    = CodeProduct
        item['CodeProducer']   = CodeProducer
        item['Description']    = Description

        yield item


    def parseText(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0|р", '', soup.get_text()).strip()
