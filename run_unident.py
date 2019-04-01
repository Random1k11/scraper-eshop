from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from unident.spiders.unident import UnidentshopSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(UnidentshopSpider)
process.start()
