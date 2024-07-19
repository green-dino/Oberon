## Script

from dynamicserialize.dstypes.com.oberon.uf.common.dataplugin.gfe.slice import AbstractGridSlice


class DiscreteGridSlice(AbstractGridSlice):

    def __init__(self):
        super(DiscreteGridSlice, self).__init__()
        self.discreteGrid = None
        self.keys = []

    def getDiscreteGrid(self):
        return self.discreteGrid

    def setDiscreteGrid(self, discreteGrid):
        self.discreteGrid = discreteGrid
        
    def getNumPyGrid(self):
        return (self.discreteGrid.getNumPyGrid(), self.key)

    def getKeys(self):
        return self.keys

    def setKeys(self, keys):
        self.keys = keys
