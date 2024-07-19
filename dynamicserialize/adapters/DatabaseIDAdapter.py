##Script


#
# Adapter for com.oberon.uf.common.dataplugin.gfe.db.objects.DatabaseID
#  
#    


from dynamicserialize.dstypes.com.oberon.uf.common.dataplugin.gfe.db.objects import DatabaseID

ClassAdapter = 'com.oberon.uf.common.dataplugin.gfe.db.objects.DatabaseID'

def serialize(context, dbId):
    context.writeString(str(dbId))
    
def deserialize(context):
    result = DatabaseID(context.readString()) 
    return result