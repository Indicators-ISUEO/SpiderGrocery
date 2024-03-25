import scrapy
from Product import Product

class FreshThymeSpider(scrapy.Spider):
    name = 'Fresh Thyme Market Spider'
    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("ITEM_PIPELINES", {
            "pipeline.FreshThyme.FreshThyme": 30,
        })
        
    def start_requests( self ):
        
        products = ["Carrots", "green onions", "potatoes", "organic spinach", "fresh spinach", "lettuce", "tomato heirloom", "tomato slicers", "tomato cherry", "strawberries",
                    "raspberries", "mushrooms", "egg large", "egg medium", "chicken whole", "beef steak", "beef whole", "pork bacon"]
        for product in products:
            url = 'https://ww2.freshthyme.com/sm/planning/rsid/951/results?q={0}'.format(product)
            yield scrapy.Request( url = url, callback = self.cardsParse, meta={'index': 0, 'url': url, 'type': product})

    def cardsParse(self, response):
        #Failsafe for links
        try:
            #grabs the store location
            storeXpath = '//*[contains(@class,"HeaderSubtitle")]/text()'
            store = response.xpath(storeXpath).extract_first()
            #grabs all cards from list and saves the link to follow
            xpath = '//*[contains(@class,"Listing")]/div/a/@href'
            type = response.meta.get('type')
            listCards = response.xpath(xpath)
            for url in listCards:
                yield response.follow( url = url, callback = self.itemParse, meta={'store': store, 'index': response.meta.get('index'), 'url': response.meta.get('url'), 'type': type})
        except AttributeError:
           pass
    
    def itemParse(self, response):
        #xpaths to extract 
        nameXpath = '//*[contains(@class, "PdpInfoTitle")]/text()'
        priceXpath = '//*[contains(@class, "PdpMainPrice")]/text()'
        prevWeightXpath = '//*[contains(@class, "PdpUnitPrice")]/text()'
        name, price, weight = ('', '', '')
        for nameExr in response.xpath(nameXpath):
            name = name + "-"+ nameExr.get()
        for priceExr in response.xpath(priceXpath):
            price = price + "-"+ priceExr.get()
        for weightExr in response.xpath(prevWeightXpath):
            weight = weight + "-"+ weightExr.get()
        url = response.meta.get('url')
        type = response.meta.get('type')
        product = Product()
        if type.lower() not in name.lower():
            return
        product['product'] = name
        product['current_price'] = price
        product['original_price'] = price
        product['weight'] = weight
        checkString = name.lower().replace(' ', '')
        if '1each' in checkString or '12each' in checkString:
            product['true_amount'] = f"{1} dz"
            product['amount_in_dz'] = 1.0
        elif '1.5each' in checkString:
            product['true_amount'] = f"{1.5} dz"
            product['amount_in_dz'] = 1.5
        product = self.setLocationalData(product=product, storeLocation=response.meta.get('store'))
        product['source'] = 'Fresh Thyme Market'
        return product
        
    def setLocationalData(self, product, storeLocation):
        store = storeLocation.lower().replace(' ', '')
        if 'westdesmoines' in store:
            product['address'] = '2900 University Ave. Suite 240'
            product['state'] = 'IA'
            product['city'] = 'West Des Moines'
            product['zip'] = '50266'    
        elif 'davenport' in store:
            product['address'] = '2130 E. Kimberly Rd.'
            product['state'] = 'IA'
            product['city'] = 'Davenport'
            product['zip'] = '52807'    
        return product
