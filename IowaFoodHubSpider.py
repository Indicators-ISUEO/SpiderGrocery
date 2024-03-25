import scrapy
from DSPG_Cleaner import DataCleaner # This is to handle the cleaning of data
from Product import Product


class IowaFoodHubSpider(scrapy.Spider):
    name = 'Iowa Food Hub'
    # currentDate = str(datetime(datetime.today().year, datetime.today().month, datetime.today().day))[:-8]
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
            url = 'https://iowa-food-hub.myshopify.com/search?q={0}'.format(product)
            yield scrapy.Request( url = url, callback = self.iowaFoodHubSearch, meta={'type': product})

    def iowaFoodHubSearch(self, response):
        #Failsafe for links
        try:
            #grabs all cards from list and saves the link to follow
            xpath = '//*[@id="MainContent"]//a[contains(@class,"list-view-item")]/@href'
            linkList = response.xpath(xpath)
            productType = response.meta.get('type')
            for url in linkList:
                yield response.follow( url = url, callback = self.iowaFoodHubBacon, meta={'type': productType}, dont_filter=True )
        except AttributeError:
           pass

    def iowaFoodHubBacon(self, response):
        #validating the name. 
        #We want to validate the name first before we load the cleaner for speed
        nameXpath = '//*[@id="ProductSection-product-template"]//*[contains(@class, "product-single__title")]/text()'
        product = Product()
        productType = response.meta.get('type')
        productname = response.xpath(nameXpath).extract_first()   
        if not productname:
            return 
        if productType.lower() not in productname.lower():
            return
        
        #load cleaner template
        clean = DataCleaner()
        product['product'] = productname
        #The other areas we are interested in
        venderXpath = '//*[@id="ProductSection-product-template"]//*[contains(@class, "product-single__vendor")]/text()'
        priceXpath = '//*[@id="ProductPrice-product-template"]/text()'
        product['current_price'] = response.xpath(priceXpath).extract_first().strip()
        product['brand'] = response.xpath(venderXpath).extract_first().strip()
        product['vendor'] = response.xpath(venderXpath).extract_first().strip()
        #getting the product discription
        discXpath = '//*[@id="ProductSection-product-template"]//*[contains(@class, "product-single__description") and @itemprop="description"]/descendant-or-self::text()'
        description = response.xpath(discXpath).getall()
        # remove leading and trailing whitespace from each string
        description = [text.strip() for text in description]
        # remove empty strings
        description = list(filter(None, description))
        # join the strings into a single string
        descriptionText = " ".join(description)
        unit = clean.findWeightUnit(descriptionText)
        if not unit:
            unit = clean.findWeightUnit(product['product'])
        product['weight'] = unit
        product['weight_lbs'] = clean.ozToLb(product['weight'])
        product = self.setLocationalData(product)
        product['source'] = 'Iowa Food Hub'
        return product
            
    def setLocationalData(self, product):
        product['address'] = '200 Railroad Street'
        product['state'] = 'IA'
        product['city'] = 'Decorah'
        product['zip'] = '52101'    
        return product 
    