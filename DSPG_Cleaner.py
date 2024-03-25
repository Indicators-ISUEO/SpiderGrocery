# from DSPG_SpiderErrors import DataCleanerError
from DSPG_SpiderErrors import StringValueExtractionError
from datetime import datetime
import re

#This is a helper class to reduce duplicate code in the DataCleaner class
class DataCleaner():               
    # def LoadDataSet(self, inputIndex, url):
    #     self.productIndex = inputIndex
    #     if self.productIndex == 0:
    #         self.Data = {'Product': None,
    #                      'Current Price': None,
    #                      'Orignal Price': None,
    #                      'Weight in lbs': None,
    #                      'True Weight': None,
    #                      'Brand': None,
    #                      'State': None, 
    #                      'City': None, 
    #                      'Zip Code': None,
    #                      'Source': None
    #                     }
    #     elif self.productIndex == 1:
    #         self.Data = {'Product': None,
    #                      'Current Price': None,
    #                      'Orignal Price': None,
    #                      'Weight in lbs': None,
    #                      'True Weight': None,
    #                      'Brand': None,
    #                      'State': None, 
    #                      'City': None, 
    #                      'Zip Code': None,
    #                      'Source': None
    #                     }
    #     elif self.productIndex == 2 or self.productIndex == 3:
    #         self.Data = {'Product': None,
    #                      'Current Price': None,
    #                      'Orignal Price': None,
    #                      'Weight in lbs': None,
    #                      'True Weight': None,
    #                      'Brand': None,
    #                      'State': None, 
    #                      'City': None, 
    #                      'Zip Code': None,
    #                      'Source': None
    #                     }
        # else:
            # raise DataCleanerError(inputIndex)

    # def cleanPricing(self):
    #     price = ''.join(c for c in self.Data['Current Price'] if c.isdigit() or c == '.')
    #     if len(price) == 0:
    #         return
    #     self.Data['Current Price'] = float(price)
    #     if self.Data['Orignal Price'] == None:
    #         self.Data['Orignal Price'] = self.Data['Current Price']
    #         return
    #     price = ''.join(c for c in self.Data['Orignal Price'] if c.isdigit() or c == '.')
    #     if len(price) == 0:
    #         self.Data['Orignal Price'] = self.Data['Current Price']
    #     else:
    #         self.Data['Orignal Price'] = float(price)
    
    # def baconModifications(self):
    #     #Finds True Weight if not available 
    #     if(self.Data['True Weight'] == None):
    #         self.Data['True Weight'] = self.findWeight()
    #     #Sets the Weight in lbs if possible
    #     if(self.Data['True Weight'] != None):
    #         self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])
    #         #On the very rare occasion the True weight doesnt help us (This does happen)
    #         if not self.Data['Weight in lbs']:
    #             self.Data['True Weight'] = self.findWeight()
    #             self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])

    def ozToLb(self, input):
        if input == None:
            return None
        weight = str(input).lower()
        if 'oz' in weight:
            unit = self.stringValueExtraction(weight, 'oz') 
            return (unit / 16.0) if unit else 0.0625
        elif 'lbs' in weight:
            unit = self.stringValueExtraction(weight, 'lb')
            return unit if unit else 1.0
        elif '/lb' in weight:
            return 1.0
        elif 'lb' in weight:
            unit = self.stringValueExtraction(weight, 'lb')
            return unit if unit else 1.0 
        return None

    #If no weight is given we look at other places that could have what we need
    #This Determines if a list talking about weights in ounces or pounds.
    def findWeight(self):
        #Checking these places for clues
        checkLocations = [self.Data['Current Price'], self.Data['Product'], self.Data['Orignal Price']]
        possible = []
        for string in checkLocations:
            if string == None: 
                continue
            unit = self.findWeightUnit(string)
            if unit == None: 
                #Failsafe
                continue
            if "/ea" in unit:
                possible.append(unit)
            else:
                return unit
        return next((item for item in possible if item is not None), None)
    
    
    def findWeightUnit(self, string):
        string = string.lower().replace(' ', '') # convert to lowercase and remove spaces
        if 'pound' in string:
            output = self.stringValueExtraction(string, 'pound')
            if output:
                return f"{output} lb"
        if 'ounce' in string:
            output = self.stringValueExtraction(string, 'ounce')
            if output:
                return f"{output} oz"      
        if 'lbs' in string:
            output = self.stringValueExtraction(string, 'lbs')
            if output:
                return f"{output} lb"  
        if '/lb' in string:
            output = self.stringValueExtraction(string, '/lb')
            if output:
                return f"{output}/lb"  
        if 'lb' in string:
            output = self.stringValueExtraction(string, 'lb')                
            if output:
                if 'lbbag'in string:
                    return f"{output} lb bag"  
                return f"{output} lb"  
        if 'oz' in string:
            output = self.stringValueExtraction(string, 'oz')
            if output:
                return f"{output} oz"         
        if '/ea' in string:
            output = self.stringValueExtraction(string, '/ea')
            if output:
                return f"{output}/ea" 
        if 'each' in string:
            output = self.stringValueExtraction(string, 'each')
            if output:
                if 'pint-' in string:
                    return f"pint - {output} each" 
                return f"{output} each" 
        return None
        
    #Tomatoes are tricky 
    # def tomatoesModifications(self, weight):
    #     #We can extract Organic from the name
    #     if self.Data['Organic'] == None:
    #         name = self.Data['Product'].lower().replace(' ', '')
    #         nameSpace = self.Data['Product'].lower() + " "
    #         if 'organic' in name:
    #             self.Data['Organic'] = True
    #         if ' og ' in nameSpace:
    #             self.Data['Organic'] = True  
    #         if '*org*' in name:
    #             self.Data['Organic'] = True  
            
    #     #This part is for Weight
    #     if self.Data['True Weight'] != None:
    #         self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])
    #         return
    #     if weight == None:
    #         string = self.findWeight()
    #         if string == None:
    #             return
    #         elif '/lb' in string.lower().replace(' ', ''):
    #             self.Data['True Weight'] = string
    #             self.Data['Weight in lbs'] = 1.0
    #             return
    #         else:
    #             self.Data['True Weight'] = string
    #     else:
    #         self.Data['True Weight'] = weight
    #     self.Data['Weight in lbs'] = self.ozToLb(self.Data['True Weight'])
        
    #Helper to reduce code. Splits the string and returns the float value 
    def stringValueExtraction(self, string, stringType):
        if string == None or stringType == None:
            raise StringValueExtractionError (string, stringType)
        string = string.lower().replace(' ', '')
        pattern = rf"(\d+\.\d+|\d+/\d+|\d+)(?={stringType})"
        matches = re.findall(pattern, string)
        unit =  [eval(match) for match in matches]
        return next((item for item in reversed(unit) if item is not None), None)
        
    # def EggFinder(self, string):
    #     if string == None:
    #         return False
    #     string = string.lower().replace(' ', '') # convert to lowercase and remove spaces
    #     if 'halfdozen' in string:
    #         self.Data['True Amount'] = f"{0.5} dz"  
    #         self.Data['Amount in dz'] = 0.5
    #         return True
    #     if 'dozen' in string:
    #         amount = self.stringValueExtraction(string, 'dozen')
    #         if amount == None:
    #             self.Data['True Amount'] = f"{1} dz"
    #             self.Data['Amount in dz'] = 1.0
    #             return True
    #         self.Data['True Amount'] = f"{amount} dz"  
    #         self.Data['Amount in dz'] = amount
    #         return True 
    #     if 'dz' in string:
    #         amount = self.stringValueExtraction(string, 'dz')
    #         self.Data['True Amount'] = f"{amount} dz"
    #         self.Data['Amount in dz'] = amount
    #         return True
    #     if 'ct' in string:
    #         amount = self.stringValueExtraction(string, 'ct')
    #         self.Data['True Amount'] = f"{amount} ct"  
    #         self.Data['Amount in dz'] = amount / 12
    #         return True
    #     if 'ea' in string:
    #         amount = self.stringValueExtraction(string, 'ea')
    #         self.Data['True Amount'] = f"{amount} ea"  
    #         self.Data['Amount in dz'] = amount / 12
    #         return True
    #     if 'pk' in string:
    #         amount = self.stringValueExtraction(string, 'pk')
    #         self.Data['True Amount'] = f"{amount} pk"  
    #         self.Data['Amount in dz'] = amount / 12
    #         return True
    #     if 'pack' in string:
    #         amount = self.stringValueExtraction(string, 'pack')
    #         self.Data['True Amount'] = f"{amount} pack" 
    #         self.Data['Amount in dz'] = amount / 12
    #         return True
    #     return False

    # #Eggs don't have weight so we use amount
    # def eggModifications(self):
    #     if self.Data['True Amount'] == None:
    #         checkLocations = [self.Data['Product'], self.Data['Current Price'], self.Data['Orignal Price']]
    #         for string in checkLocations:
    #             if(self.EggFinder(string)):
    #                 return
    #     else:
    #         string = self.Data['True Amount'].lower().replace(' ', '')
    #         if 'dozen' in string:
    #             amount = self.stringValueExtraction(string, 'dozen')
    #             if amount == None:
    #                 self.Data['Amount in dz'] = 1.0
    #                 return
    #             self.Data['Amount in dz'] = amount
    #         elif 'dz' in string:
    #             self.Data['Amount in dz'] = self.stringValueExtraction(string, 'dz')
    #         elif 'ct' in string:
    #             self.Data['Amount in dz'] = self.stringValueExtraction(string, 'ct') / 12
    #         elif 'ea' in string:
    #             self.Data['Amount in dz'] = self.stringValueExtraction(string, 'ea') / 12
    #         elif 'pk' in string:
    #             self.Data['Amount in dz'] = self.stringValueExtraction(string, 'pk') / 12
    #         elif 'pack' in string:
    #             self.Data['Amount in dz'] = self.stringValueExtraction(string, 'pack') / 12
