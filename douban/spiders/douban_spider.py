import scrapy
from douban.items import Film 
import re


class DouBan(scrapy.Spider):
    name = "douban"
    start_urls = ["https://www.douban.com/doulist/30299/"]

    def parse(self, response):
        page_total = response.selector.xpath("//span[@class='thispage']/@data-total-page").extract()
        if page_total:
            page_total = int(page_total[0])
            for i in range(page_total):
                url = "https://www.douban.com/doulist/30299/?start={}&sort=seq&playable=0&sub_type=".format(i*25)
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        films_box = response.selector.xpath("//div[@class='doulist-item']/div[@class='mod']")
        films_body = films_box.xpath("div[@class='bd doulist-subject']")
        films_name = films_body.xpath("div[@class='title']/a/text()[last()]").extract()
        films_score = films_body.xpath("div[@class='rating']/span[@class='rating_nums']/text()").extract()
 
        rating_users = films_body.xpath("div[@class='rating']/span[3]/text()").extract()
        number_pattern = "\d+"
        rating_users = [re.search(number_pattern, i).group() for i in rating_users]
        films_abstract = films_body.xpath("div[@class='abstract']")
        for idx, name in enumerate(films_name):
            name = name.strip()
            film = Film()
            film["name"] = name
            film["score"] = films_score[idx]
            film["rating_users"] = rating_users[idx]
            info_list = films_abstract[idx].xpath("text()").extract()
            info_list = [i.strip() for i in info_list]
            for s in info_list:
                if s.startswith("导演"):
                    film["director"] = s[4:]
                elif s.startswith("主演"):
                    film["starring"] = s[4:]
                elif s.startswith("类型"):
                    film["film_type"] = s[4:]
                elif s.startswith("制片国家/地区"):
                    film["country_regin"] = s[9:]
                elif s.startswith("年份"):
                    film["year"] = s[4:]
            yield film
    
