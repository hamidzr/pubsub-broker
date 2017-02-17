class DataStorage(object):
    """docstring for DataStorage"""
    def __init__(self,address):
        super(DataStorage, self).__init__()
        self.data = {}
        self.address = address
        
    def __str__(self):
        return self.address # whatever we wanna hash
    """ set a key value
    returns true if succeed """
    def set(self,key,value):
        self.data[key] = value
        return key, value + ' successfully added to DataStorage ' + self.address

    def displayData(self):
        return self.address + ' ' + self.data.__str__()
    
    def get(key):
        return self.data[key]