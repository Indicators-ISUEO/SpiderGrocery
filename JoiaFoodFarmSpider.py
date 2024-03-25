import scrapy
from DSPG_Cleaner import DataCleaner # This is to handle the cleaning of data
from Product import Product

class JoiaFoodFarmSpider(scrapy.Spider):
    name = 'Joia Food Farm'
    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("ITEM_PIPELINES", {
            "pipeline.FreshThyme.FreshThyme": 30,
        })
    def start_requests( self ):
        #Bacon Scraper part
        products = ["Beef", "Chicken", "Eggs", "Garlic", "Fruit", "Lamb", "Mushrooms", "Pork", "Turkey", "Vegetables"]
        for product in products:
            url = 'https://www.joiafoodfarm.com/farmstore?category={0}'.format(product)
            yield scrapy.Request( url = url, callback = self.JoiaFoodFarmSearch, meta={'type': product})

    def JoiaFoodFarmSearch(self, response):
        #Failsafe for links
        try:
            #grabs all cards from list and saves the link to follow
            xpath = '//main//*[contains(@class, "ProductList-grid")]//*[contains(@class, "ProductList-item-link")]/@href'
            linkList = response.xpath(xpath)
            productType = response.meta.get('type')
            for url in linkList:
                yield response.follow( url = url, callback = self.JoiaFoodFarmProduct, meta={'type': productType}, dont_filter=True )
        except AttributeError:
           pass

    def JoiaFoodFarmProduct(self, response):
        product = Product()
        nameXpath = '//*[contains(@class, "ProductItem-summary")]//h1[contains(@class, "ProductItem-details-title")]/text()'
        name = response.xpath(nameXpath).extract_first()
        
        productType = response.meta.get('type')
        if productType.lower() not in name.lower():
            return          
        #load cleaner template
        clean = DataCleaner()
        product['product'] = name.strip()
        
        #The other areas we are interested in
        priceXpath = '//*[contains(@class, "ProductItem-summary")]//*[contains(@class, "product-price")]/text()'    
        product['current_price'] = response.xpath(priceXpath).extract_first().strip()
        
        #getting the product discription
        discXpath = '//*[contains(@class, "ProductItem-summary")]//*[contains(@class, "ProductItem-details-excerpt")]/descendant-or-self::text()'
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
        # clean.cleanPricing()
        product = self.setLocationalData(product)
        product['source'] = 'Joia food farm'
        product['vendor'] = 'Joia food farm'
        return product

    def setLocationalData(self, product):
        #Brands dont change from this site so we add them here
        product['brand'] = 'Joia food farm'
        product['address'] = '2038 March Avenue'
        product['state'] = 'IA'
        product['city'] = 'Charles City'
        product['zip'] = '50616'    
        return product 
    