import scrapy

from scrapy.loader import ItemLoader

from ..items import AlrayanItem
from itemloaders.processors import TakeFirst


class AlrayanSpider(scrapy.Spider):
	name = 'alrayan'
	start_urls = ['https://www.alrayan.com/english/media-center/news-and-press-releases']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "phMainContent_listing1_divListContent")]//*[contains(concat( " ", @class, " " ), concat( " ", "listingTitle", " " ))]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		if 'pdf' in response.url:
			return
		title = response.xpath('//div[@class="textEditor"]/h3/text()').get()
		description = response.xpath('//div[@class="contentSpace"]//text()[normalize-space()] | //div[@class="textEditor"]/p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="textEditor"]/div[@class="listingDate"]/text()').get()

		item = ItemLoader(item=AlrayanItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
