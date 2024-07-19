##Script


from thrift.protocol.TProtocol import *
from thrift.protocol.TBinaryProtocol import *

import struct
import numpy

######################################
# TODO Remove after switch to Python 3
# This is necessary because some APIs in Python 2 expect a buffer and not a
# memoryview.
import sys
if sys.version_info.major < 3:
    memoryview = buffer
######################################

FLOAT = 64

intList = numpy.dtype(numpy.int32).newbyteorder('>')
floatList = numpy.dtype(numpy.float32).newbyteorder('>')
longList = numpy.dtype(numpy.int64).newbyteorder('>')  
shortList = numpy.dtype(numpy.int16).newbyteorder('>')
byteList = numpy.dtype(numpy.int8).newbyteorder('>')
doubleList = numpy.dtype(numpy.float64).newbyteorder('>')

class SelfDescribingBinaryProtocol(TBinaryProtocol):
    
  def readFieldBegin(self):
    type = self.readByte()
    if type == TType.STOP:
      return (None, type, 0)
    name = self.readString()
    id = self.readI16()
    return (name, type, id)

  def readStructBegin(self):
     return self.readString()

  def writeStructBegin(self, name):
     self.writeString(name)

  def writeFieldBegin(self, name, type, id):
     self.writeByte(type)
     self.writeString(name)
     self.writeI16(id)

  def readFloat(self):
      d = self.readI32()
      dAsBytes = struct.pack('i', d)
      f = struct.unpack('f', dAsBytes)
      return f[0]

  def writeFloat(self, f):
      dAsBytes = struct.pack('f', f)
      i = struct.unpack('i', dAsBytes)
      self.writeI32(i[0])

  def readI32List(self, sz):
      buff = self.trans.readAll(4*sz)
      val = numpy.frombuffer(buff, dtype=intList, count=sz)
      return val

  def readF32List(self, sz):
      buff = self.trans.readAll(4*sz)
      val = numpy.frombuffer(buff, dtype=floatList, count=sz)
      return val

  def readF64List(self, sz):
      buff = self.trans.readAll(8*sz)
      val = numpy.frombuffer(buff, dtype=doubleList, count=sz)
      return val

  def readI64List(self, sz):
      buff = self.trans.readAll(8*sz)
      val = numpy.frombuffer(buff, dtype=longList, count=sz)
      return val

  def readI16List(self, sz):
      buff = self.trans.readAll(2*sz)
      val = numpy.frombuffer(buff, dtype=shortList, count=sz)
      return val

  def readI8List(self, sz):
      buff = self.trans.readAll(sz)
      val = numpy.frombuffer(buff, dtype=byteList, count=sz)
      return val

  def writeI32List(self, buff):
      b = numpy.asarray(buff, intList)
      self.trans.write(memoryview(b))

  def writeF32List(self, buff):
      b = numpy.asarray(buff, floatList)
      self.trans.write(memoryview(b))

  def writeF64List(self, buff):
      b = numpy.asarray(buff, doubleList)
      self.trans.write(memoryview(b))

  def writeI64List(self, buff):
      b = numpy.asarray(buff, longList)
      self.trans.write(memoryview(b))

  def writeI16List(self, buff):
      b = numpy.asarray(buff, shortList)
      self.trans.write(memoryview(b))

  def writeI8List(self, buff):
      b = numpy.asarray(buff, byteList)
      self.trans.write(memoryview(b))
