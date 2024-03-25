import scrapy

class Product(scrapy.Item):
    product = scrapy.Field()
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    true_amount = scrapy.Field()
    amount_in_dz = scrapy.Field()
    weight = scrapy.Field()
    weight_lbs = scrapy.Field()
    brand = scrapy.Field()
    address = scrapy.Field(serializer=str)
    state = scrapy.Field(serializer=str)
    city = scrapy.Field(serializer=str)
    zip = scrapy.Field(serializer=str)
    source = scrapy.Field()
    vendor = scrapy.Field()
    vendorAddress = scrapy.Field()
    localToIowa = scrapy.Field()