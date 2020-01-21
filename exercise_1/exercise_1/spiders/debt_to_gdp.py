# -*- coding: utf-8 -*-
import scrapy
from colorama import init
from termcolor import colored
import logging


class DebtToGdpSpider(scrapy.Spider):
    init()
    name = "debt_to_gdp"
    allowed_domains = ["worldpopulationreview.com"]
    start_urls = [
        "http://worldpopulationreview.com/countries/countries-by-national-debt/"
    ]

    def parse(self, response):
        countries = response.xpath("(//tr)")
        for country in countries:
            country_name = country.xpath(".//td[1]/a/text()").get()
            link = country.xpath(".//td[1]/a/@href").get()
            ratio = country.xpath(".//td[2]/text()").get()
            population = country.xpath(".//td[3]/text()").get()
            data = {
                "country_name": country_name,
                "ratio": ratio,
                "population": population,
            }
            logging.info(colored(data, "yellow"))
            yield data

    def parse_country(self, response):
        logging.info(colored(response.request.meta, "yellow"))
