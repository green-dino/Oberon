## Script


import abc

class PersistableDataObject(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        self.traceId = None

    def getTraceId(self):
        return self.traceId

    def setTraceId(self, traceId):
        self.traceId = traceId

