## Script

# File auto-generated against equivalent DynamicSerialize Java class

import os
import uuid
from dynamicserialize.dstypes.com.oberon.uf.common.localization.stream import AbstractLocalizationStreamRequest
from dynamicserialize.dstypes.com.oberon.uf.common.auth.user import User


class LocalizationStreamPutRequest(AbstractLocalizationStreamRequest):

    def __init__(self):
        super(LocalizationStreamPutRequest, self).__init__()
        self.id = str(uuid.uuid4())
        self.bytes = None
        self.end = None
        self.offset = None
        self.localizedSite = None

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getBytes(self):
        return self.bytes

    def setBytes(self, bytes):
        self.bytes = bytes

    def getEnd(self):
        return self.end

    def setEnd(self, end):
        self.end = end

    def getOffset(self):
        return self.offset

    def setOffset(self, offset):
        self.offset = offset

    def getLocalizedSite(self):
        return self.localizedSite

    def setLocalizedSite(self, localizedSite):
        self.localizedSite = localizedSite

