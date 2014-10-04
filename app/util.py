class SafeDict(dict):
    _keys = []

    def __init__(self, d={}):
        _keys = d.keys()
        for key in _keys:
            self.__setitem__(key, d[key])

    def __getitem__(self, key):
        if key not in self._keys:
            return 0
        return dict.__getitem__(self,key)
        
    def __setitem__(self, key, value):
        self._keys.append(key)
        dict.__setitem__(self,key,value)
