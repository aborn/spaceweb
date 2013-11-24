# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SpacewebItem(Item):
    # define the fields for your item here like:
    # name = Field()
    desc = Field()
    link = Field()
    pass
