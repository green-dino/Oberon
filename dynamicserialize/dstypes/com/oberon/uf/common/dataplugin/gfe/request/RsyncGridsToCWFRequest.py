## Script
#    


from dynamicserialize.dstypes.com.oberon.uf.common.dataplugin.gfe.request import AbstractGfeRequest


class RsyncGridsToCWFRequest(AbstractGfeRequest):

    def __init__(self, siteId=None):
        super(RsyncGridsToCWFRequest, self).__init__()
        if siteId is not None:
            self.siteID = str(siteId)
