## Script

# File auto-generated against equivalent DynamicSerialize Java class

from dynamicserialize.dstypes.com.oberon.uf.common.auth.resp import AbstractFailedResponse


class UserNotAuthorized(AbstractFailedResponse):

    def __init__(self):
        super(UserNotAuthorized, self).__init__()
        self.message = None

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message
