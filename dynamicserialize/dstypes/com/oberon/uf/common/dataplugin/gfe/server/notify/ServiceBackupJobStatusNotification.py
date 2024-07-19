## Script
#    


from .GfeNotification import GfeNotification

class ServiceBackupJobStatusNotification(GfeNotification):

    def __init__(self):
        super(ServiceBackupJobStatusNotification, self).__init__()
        self.name = None
        self.state = "UNKNOWN"

    def __str__(self):
        msg = "name: " + str(self.name)
        msg += '\n' + "state: " + str(self.state)
        return msg

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state
        
