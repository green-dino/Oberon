## Script

# File auto-generated against equivalent DynamicSerialize Java class

import abc
import os
from dynamicserialize.dstypes.com.oberon.uf.common.auth.user import User

class AbstractLocalizationStreamRequest(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.context = None
        self.fileName = None
        self.myContextName = None
        self.user = User()

    def getContext(self):
        return self.context

    def setContext(self, context):
        self.context = context

    def getFileName(self):
        return self.fileName

    def setFileName(self, fileName):
        if fileName[0] == os.sep:
            fileName = fileName[1:] 
        self.fileName = fileName
        
    def getMyContextName(self):
        return self.myContextName

    def setMyContextName(self, contextName):
        self.myContextName = str(contextName)

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user

