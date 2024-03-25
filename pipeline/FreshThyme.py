from itemadapter import ItemAdapter
import csv
from datetime import datetime
from Product import Product
import os
import pandas as pd
import requests

class FreshThyme:
    def open_spider(self, spider):
        self.vendorList = pd.read_csv("vendorList.csv", header=None, index_col=0)
        product = Product()
        fieldnames = list(product.fields.keys())
        currentDate = str(datetime(datetime.today().year, datetime.today().month, datetime.today().day))[:-9]
        filePath = "data/{0}.csv".format(currentDate)
        fileExist = os.path.isfile(filePath)
        self.csvfile = open(filePath, "a",newline='')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames) 
        if not fileExist:
            self.writer.writeheader()
                

    def close_spider(self, spider):
        self.csvfile.close()

    def process_item(self, item, spider):
        print("{0}- {1}".format(item['product'], item['source']))
        
        item['localToIowa'] = False
        
        # set vendor to initial if not set
        if 'vendor' not in item:
            item['vendor'] = ''
            
        product = item['product'] if not item['vendor'] else item['vendor']
        df = self.vendorList.filter(like=product, axis = 0)
        if df.size > 0:
            item['localToIowa'] = True
        else:
            url = 'https://services-here.aws.mapquest.com/v1/search?query={0}&count=5&prefetch=5&client=yogi&clip=none'.format(product)
            headers = {'Host': 'services-here.aws.mapquest.com', 'User-Agent': 'PostmanRuntime/7.37.0'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                results = data['results']
                if results:
                    address = results[0]['address']
                    region, locality, address1, postalCode = ('', '', '', '')
                    if 'region' in address:
                        region = address['region']
                        if region == 'IA':
                            item['localToIowa'] = True
                    if 'locality' in address:
                        locality = address['locality']
                    if 'address1' in address:
                        address1 = address['address1']
                    if 'postalCode' in address:
                        postalCode = address['postalCode']
                    item['vendorAddress'] = "{0} {1} {2} {3}".format(address1, locality, region, postalCode)
                
        item = ItemAdapter(item).asdict()
        self.writer.writerow(item)
        test = ''
        # line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # self.file.write(line)
        # return item
    