## Script
#



class LockTable(object):

    def __init__(self):
        self.locks = None
        self.wsId = None
        self.parmId = None

    def getLocks(self):
        return self.locks

    def setLocks(self, locks):
        self.locks = locks

    def getWsId(self):
        return self.wsId

    def setWsId(self, wsId):
        self.wsId = wsId

    def getParmId(self):
        return self.parmId

    def setParmId(self, parmId):
        self.parmId = parmId
        
    def __repr__(self):
        msg = "ParmID: " + str(self.parmId)        
        msg += " LockTable WsId: " + str(self.wsId)
        for i in self.locks:                
            msg += "\n  Lock: " + str(i)            
        return msg

