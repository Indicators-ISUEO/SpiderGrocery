
# These are all Errors to protect you from wasting time in trying to figure out whats wrong
# It is imperative that these classes is expanded upon and used in future development  

class ProductsError(Exception):
    def __init__(self):
        self.message = "The number of Data frame added and number of products added do not match. \n Please check this in the Products class (DSPG_Products)"

class DataCleanerError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = f"Data frame not found for input index ({index}) in (DSPG_Cleaner -> Class(DataCleaner) -> function(LoadDataSet)). \n Either the input was out of range or the Data cleaning process for the product wasn't implemented just yet."

class DataFormatingError(Exception):
    def __init__(self, index):
        self.index = index
        self.message = f"Data frame not found for input index ({index}) in (Current Spider -> Class(DataFormater) -> function(cleanUp)). \n Either the input was out of range or the Data cleaning process for the product wasn't implemented just yet."

class StoreLocationError(Exception):
    def __init__(self, index):
        self.message = f"Store index not found for index ({index}) in (Current Spider -> Class(DataFormater) -> function(setLocationalData))."

class StringValueExtractionError(Exception):
    def __init__(self, string, stringType):
        self.message = f" In (DSPG_Cleaner -> Class(DataCleaner) -> function(stringValueExtraction)). Something when wrong String({string}) Spliting({stringType})"

class ProductFinderError(Exception):
    def __init__(self, string):
        self.message = f" Could not find product for ({string})"
    
# Helpful to have when you need to stop the program and throw an error
class DebugError(Exception):
    def __init__(self, values):
        self.message = f"({values})\n Stopped Something when wrong!"
