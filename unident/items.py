# -*- coding: utf-8 -*-

import scrapy


class UnidentItem(scrapy.Item):

    Title =          scrapy.Field()
    Price =          scrapy.Field()
    Brand =          scrapy.Field()
    CodeProduct =    scrapy.Field()
    CodeProducer =   scrapy.Field()
    Description =    scrapy.Field()
