# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country/"
    ]

    def parse(self, response):
        """
        :param response: The response object
        :type response: Response
        """
        countries = response.xpath("//td/a")
        for country in countries:
            # '.' introduces a relative location path, starting at the context node
            # (i.e., the current Selector object from the response result)
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # following links (3 methods)
            # absolute_url = f"https://www.worldometers.info{link}" --> yield scrapy.Response(url=absolute_url)
            # absolute_url = response.urljoin(link) --> yield scrapy.Response(url=absolute_url)
            yield response.follow(url=link)
