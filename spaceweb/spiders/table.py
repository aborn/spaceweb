from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from spaceweb.items import SpacewebItem
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url

class TableSpider(BaseSpider):
    name="table"
    allowed_domains = ["wszw.hzs.mofcom.gov.cn"]
    start_urls = [
        "http://wszw.hzs.mofcom.gov.cn/fecp/fem/corp/fem_cert_stat_view_list.jsp"
    ]

    def parse(self, response):
        response = response.replace(body=response.body.replace("disabled",""))
        hxs=HtmlXPathSelector(response)
        requests = []
        start_index = 2
        end_index = 4                               # total page number is 1367
        if start_index < end_index:                 # request next pages
            el = hxs.select('//input[@name="Grid1toPageNo"]/@value')[0]
            val=int(el.extract())                   # the current page number
            newval=val+1
            print "------------- the current page is %d ------------------" % val
            print "(val=%d)---(newval=%d)" % (val,newval)
            if newval <= end_index:
                requests.append(FormRequest.from_response(response, \
                                formdata={"Grid1toPageNo":str(newval)}, \
                                dont_click=True,callback=self.parse))
                #requests.append(FormRequest.from_response(response, \
                #                formdata={"CHECK_DTE":"2006-09-14"}, \
                #                dont_click=True,callback=self.parse))
                #requests.append(FormRequest.from_response(response, \
                #                formdata={"Grid1toPageNo":newval}, \
                #                dont_click=True))
        for request in requests:
            yield request
        sites=hxs.select('//td[contains(@class,"listTableBodyTD")]/div')
        items = []
        for site in sites:
            item = SpacewebItem()
            item['desc'] = site.select('text()').extract()   
            items.append(item)                # items means each page's content

        dataSaveName="result.txt."+str(val)   # save the data to this file
        file_each=open(dataSaveName, 'w');
        for gis in items:
            if len(gis['desc']) > 0:
                file_each.write(gis['desc'][0].encode('utf8'))
                file_each.write(" # ")
            else:
                file_each.write('\n')          # next line
        file_each.close()
        start_index=start_index + 1
        print "------------ finished page %d, left %d pages ------------" \
              % (val, end_index-val)
SPIDER = TableSpider()
