
__all__ = [
    'PointAdapter',
    'StackTraceElementAdapter',
    'CalendarAdapter',
    'GregorianCalendarAdapter',
    'DateAdapter',
    'GeometryTypeAdapter',
    'CoordAdapter',
    'TimestampAdapter',
    'EnumSetAdapter',
    'FloatBufferAdapter',
    'ByteBufferAdapter',
    'JTSEnvelopeAdapter'
]

classAdapterRegistry = {}


def getAdapterRegistry():
    import pkgutil
    
    discoveredPackages = []
    # allow other plugins to contribute to adapters by dropping their adapter or
    # package into the dynamicserialize.adapters package
    for _, modname, ispkg in pkgutil.iter_modules(__path__):
        if ispkg:
            discoveredPackages.append(modname)
        else:
            if modname not in __all__:
                __all__.append(modname)
    
    registerAdapters(__name__, __all__)
    
    for pkg in discoveredPackages:
        __import__(__name__ + '.' + pkg)
    
            
def registerAdapters(package, modules):
    import sys
    if not package.endswith('.'):
        package += '.'
    for x in modules:
        exec('import ' + package + x)
        m = sys.modules[package + x]
        d = m.__dict__
        if 'ClassAdapter' in d:
            if isinstance(m.ClassAdapter, list):
                for clz in m.ClassAdapter:
                    classAdapterRegistry[clz] = m
            else:
                clzName = m.ClassAdapter
                classAdapterRegistry[clzName] = m
        else:
            raise LookupError('Adapter class ' + x + ' has no ClassAdapter field ' +
                              'and cannot be registered.')


getAdapterRegistry()
