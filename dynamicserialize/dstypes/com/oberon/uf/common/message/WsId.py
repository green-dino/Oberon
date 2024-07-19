
import struct
import socket
import os
import pwd
import threading

class WsId(object):

    def __init__(self, networkId=None, userName=None, progName=None, pid=None, threadId=None):
        self.networkId = networkId
        if networkId is None:
            self.networkId = str(struct.unpack('<L',socket.inet_aton(socket.gethostbyname(socket.gethostname())))[0])
        
        self.userName = userName
        if userName is None:
            self.userName = pwd.getpwuid(os.getuid()).pw_name
            
        self.progName = progName
        if progName is None:
            self.progName = "unknown"
        
        self.pid = pid
        if self.pid is None:
            self.pid = os.getpid()
        
        self.threadId = threadId
        if self.threadId is None:
            self.threadId = threading.current_thread().ident

    def getNetworkId(self):
        return self.networkId

    def setNetworkId(self, networkId):
        self.networkId = networkId

    def getUserName(self):
        return self.userName

    def setUserName(self, userName):
        self.userName = userName

    def getProgName(self):
        return self.progName

    def setProgName(self, progName):
        self.progName = progName

    def getPid(self):
        return self.pid

    def setPid(self, pid):
        self.pid = pid

    def getThreadId(self):
        return self.threadId

    def setThreadId(self, threadId):
        self.threadId = threadId
        
    def toPrettyString(self):        
        hostname = socket.gethostbyaddr(socket.inet_ntoa(struct.pack('<L', int(self.networkId))))[0]
        return self.userName + "@" + hostname + ":" + self.progName + ":" + str(self.pid) + ":" + str(self.threadId)
    
    def __str__(self):
        s = ":".join([self.networkId, self.userName, self.progName, str(self.pid), str(self.threadId)])
        return s
    
    def __repr__(self):
        return self.__str__()