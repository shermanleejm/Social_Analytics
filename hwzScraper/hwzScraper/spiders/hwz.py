import scrapy
import requests
from scrapy import Request
from bs4 import BeautifulSoup
from scrapy.utils.markup import remove_tags

class hwzScraper(scrapy.Spider) :
    name = 'hwz'

    start_urls = [
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2019-2020-intake-5948017.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2018-2019-intake-5697946.html",
        "http://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2017-2018-intake-5434864.html",
        "http://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2017-2018-intake-part-2-a-5630533.html",
        "http://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2016-2017-intake-5205927.html",
        "http://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2016-2017-intake-part-2-a-5433972.html",
        "http://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2015-2016-intake-4854297.html",
        "http://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2014-2015-intake-4315732.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/ntu-nus-smu-2020-2021-intake-6192001.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/suss-part-time-2020-01-intake-6045231.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/suss-part-time-2020-07-intake-6155037.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/suss-ft-sit-sutd-2019-2020-intake-5948026.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/sim-mdis-kaplan-2019-2020-intake-5973921.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/2018-intake-anyone-go-sit-interview-got-acceptance-already-5767694.html",
        "https://forums.hardwarezone.com.sg/degree-programs-courses-70/sutd-sit-unisim-2017-2018-intake-5519164.html",
        

    ]

    # def parse(self, response):
    #     for post in response.xpath("//td[@class='alt1']"):
    #         if post.xpath(".//div[@class='post_message']//text()").extract() != []:
    #             name = post.xpath
    #             msg = post.xpath(".//div[@class='post_message']//text()").extract()
    #             message = ""
    #             for word in msg:
    #                 if word.strip() != "":
    #                     message += word.replace("\r", "").replace("\t", "").replace("\n", " ")
    #             yield {
    #                 "msg" : message
    #             }

    def parse(self, response) :
        for post in response.xpath("//div[@class='post-wrapper']"):
            name = post.xpath(".//a[@class='bigusername']//text()").extract()[0]
            msg = post.xpath(".//div[@class='post_message']//text()").extract()
            ts = post.xpath(".//td[@class='thead']//text()").extract()
            timestamp = ""
            message = ""
            for word in msg:
                if word.strip() != "":
                    message += word.replace("\r", "").replace("\t", "").replace("\n", " ")
            for t in ts:
                if t.strip() != "":
                    timestamp += t.replace("\r", "").replace("\t", "").replace("\n", " ").strip()
            yield {
                "name" : name,
                "message" : message,
                "timestamp" : timestamp
            }

        # x = response.css('div.post_message')
        # for i in range(len(x)):
        #     # msg = x[i].css('::text').extract()
        #     # yield {i:' '.join([i for i in msg if i not in space])}
        #     yield {i:' '.join(x[i].css('::text').extract())}

        # yield {
        #     "link" : "https://forums.hardwarezone.com.sg" + response.xpath("//li[@class='prevnext'][2]/a/@href").extract_first()
        # }
        # next page

        next_page = response.xpath("//li[@class='prevnext'][2]/a/@href").extract_first()
        if next_page is not None:
            next_page_link = "https://forums.hardwarezone.com.sg" + next_page
            yield scrapy.Request(url=next_page_link, callback=self.parse)
        
 