import scrapy
from scrapy.linkextractors import LinkExtractor

class MainSpider(scrapy.Spider):
    name = "main"

    def __init__(self, domain, css_selector):
        self.allowed_domains = [domain]
        self.start_urls = ["https://" + domain]
        self.css_selector = css_selector

        # Print for logging information
        print(f"USING CSS SELECTOR: {css_selector}")
        print(f"SCRAPING DOMAIN: {domain}")
    
    def parse(self, response):
        whole_page_content = ""
        
        for content in response.css(self.css_selector + "::text"):
            if content != "":
                whole_page_content += str(content.get())
        
        yield {
            'content': whole_page_content,
            'url': response.url, 
        }

        le = LinkExtractor()
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)