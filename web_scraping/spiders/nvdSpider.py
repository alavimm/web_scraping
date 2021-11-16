import scrapy
from scrapy.crawler import CrawlerProcess


class nvdSpider(scrapy.Spider):
    name = "nvdSpider"

    def start_requests(self):
        urls = ['http://quotes.toscrape.com/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for item in response.css("div.quote"):
            yield{
                "text": item.css("span.text::text").get(),
                "author": item.css("small.author::text").get(),
                "tags": item.css("div.tags a.tag::text").getall()
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(nvdSpider)
    process.start()  # the script will block here until the crawling is finished
