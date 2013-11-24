from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from spaceweb.items import SpacewebItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url

class IfengSpider(BaseSpider):
    name="ifeng"
    allowed_domains = ["www.ifeng.com"]
    start_urls = ["http://www.ifeng.com"]
    def parse(self, response):
        infoFile="info.txt"
        fidFile=open(infoFile, 'w')
        hxs = HtmlXPathSelector(response)
        sites=hxs.select('/html/body/div[7]/div/div/div/div[3]')
        items = []
        for site in sites:
            item = SpacewebItem()
            item['desc'] = site.select('./h1/a').select('text()').extract()
            items.append(item)
            rootContent = site.select('./ul')
            for j in range(1,17):
                jstr="./li[%d]/a" % j
                item = SpacewebItem()
                item['desc'] = rootContent.select(jstr).select('text()').extract()
                item['link'] = rootContent.select(jstr).select('./@href').extract()
                items.append(item)
            
            for item in items:
                if len(item) > 1 and len(item['desc']) > 0 \
                   and len(item['link']) > 0:
                    print "[item:",item['desc'][0].encode('utf8'),
                    print "] url:",item['link'][0]
                    fidFile.write(item['desc'][0].encode('utf8'))
                    fidFile.write("[")
                    fidFile.write(item['link'][0])
                    fidFile.write("]")
                    fidFile.write('\n')
        fidFile.close()
SPIDER = IfengSpider()
