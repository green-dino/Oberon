## Script


from .GfeNotification import GfeNotification

class DBInvChangeNotification(GfeNotification):

    def __init__(self):
        super(DBInvChangeNotification, self).__init__()
        self.additions = None
        self.deletions = None

    def getAdditions(self):
        return self.additions

    def setAdditions(self, additions):
        self.additions = additions

    def getDeletions(self):
        return self.deletions

    def setDeletions(self, deletions):
        self.deletions = deletions

    def __str__(self):
        msg = 'Additions' + str(self.additions) + '\n'
        msg += 'Deletions' + str(self.deletions)
        return msg

