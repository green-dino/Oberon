## Script
# ----------------------------------------------------------------------------


from time import gmtime, strftime
from dynamicserialize.dstypes.java.sql import Timestamp

class CommutativeTimestamp(Timestamp):

    def __init__(self, timeInMillis=None):
        super(CommutativeTimestamp, self).__init__(timeInMillis)

