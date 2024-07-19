## Script

##


from dynamicserialize.dstypes.com.oberon.uf.common.dataplugin.gfe.request import AbstractGfeRequest

class GetSiteTimeZoneInfoRequest(AbstractGfeRequest):

    def __init__(self):
        super(GetSiteTimeZoneInfoRequest, self).__init__()
        self.requestedSiteIDs = None

    def getRequestedSiteIDs(self):
        return self.requestedSiteIDs

    def setRequestedSiteIDs(self, requestedSiteIDs):
        self.requestedSiteIDs = requestedSiteIDs

