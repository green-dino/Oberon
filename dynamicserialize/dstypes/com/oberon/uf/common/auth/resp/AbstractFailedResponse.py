## Script

# File auto-generated against equivalent DynamicSerialize Java class

import abc


class AbstractFailedResponse(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.request = None

    def getRequest(self):
        return self.request

    def setRequest(self, request):
        self.request = request

