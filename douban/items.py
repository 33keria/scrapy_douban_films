# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Film(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    rating_users = scrapy.Field()
    director = scrapy.Field()
    starring = scrapy.Field()
    film_type = scrapy.Field()
    country_regin = scrapy.Field()
    year = scrapy.Field()
