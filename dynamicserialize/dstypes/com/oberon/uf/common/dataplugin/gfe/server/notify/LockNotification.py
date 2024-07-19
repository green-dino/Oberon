## Script

from .GfeNotification import GfeNotification

class LockNotification(GfeNotification):

    def __init__(self):
        super(LockNotification, self).__init__()
        self.lockTable = None

    def getLockTable(self):
        return self.lockTable

    def setLockTable(self, lockTable):
        self.lockTable = lockTable

    def __str__(self):
        return str(self.lockTable)

