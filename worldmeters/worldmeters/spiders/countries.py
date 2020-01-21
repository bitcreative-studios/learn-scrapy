# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Response
import logging


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
            yield response.follow(
                url=link, callback=self.parse_country, meta={"country_name": name}
            )

    def parse_country(self, response):
        """
        :param response: The response object
        :type response: Response
        """
        name = response.request.meta["country_name"]
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr"
        )
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {"year": year, "population": population, "country_name": name}
