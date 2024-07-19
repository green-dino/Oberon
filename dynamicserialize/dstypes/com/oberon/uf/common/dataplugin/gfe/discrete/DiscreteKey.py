## Script




SUBKEY_SEPARATOR = '^'
AUXDATA_SEPARATOR = ':'

class DiscreteKey(object):

    def __init__(self):
        self.siteId = None
        self.subKeys = None
        self.parmID = None
        
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return SUBKEY_SEPARATOR.join(self.subKeys)
    
    def __getitem__(self, key):
        try:
            index = int(key)
        except:
            raise TypeError("list indices must be integers, not " + str(type(key)))
        if index < 0 or index > len(self.subKeys):
            raise IndexError("index out of range")
        return self.subKeys[index]
    
    def __hash__(self):
        return hash((self.parmID, self.siteId, self.subKeys))
    
    def __eq__(self, other):
        if not isinstance(other, DiscreteKey):
            return False
        if self.parmID != other.parmID:
            return False
        if self.siteId != other.siteId:
            return False
        return self.subKeys == other.subKeys
    
    def __ne__(self, other):
        return (not self.__eq__(other))
        
    @staticmethod
    def auxData(subkey):
        pos = subkey.find(AUXDATA_SEPARATOR)
        if pos != -1:
            return subkey[pos + 1:]
        else:
            return ""
        
    @staticmethod
    def baseData(subkey):
        pos = subkey.find(AUXDATA_SEPARATOR)
        if pos != -1:
            return subkey[:pos]
        else:
            return subkey

    def getSiteId(self):
        return self.siteId

    def setSiteId(self, siteId):
        self.siteId = siteId

    def getSubKeys(self):
        return self.subKeys

    def setSubKeys(self, subKeys):
        self.subKeys = subKeys

    def getParmID(self):
        return self.parmID

    def setParmID(self, parmID):
        self.parmID = parmID

