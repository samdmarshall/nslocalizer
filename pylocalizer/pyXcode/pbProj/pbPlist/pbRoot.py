import collections

import pbItem

def StringCmp(obj1, obj2):
    if obj1 > obj2:
        return 1
    elif obj1 == obj2:
        return 0
    else:
        return -1

def KeySorter(obj1, obj2):
    if str(obj1) == 'isa':
        return -1
    elif str(obj2) == 'isa':
        return 1
    else:
        return StringCmp(str(obj1), str(obj2))

class pbRoot(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.key_storage = list()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __internalKeyCheck(self, key):
        safe_key = key
        if type(safe_key) == str:
            safe_key = pbItem.pbItemResolver(safe_key, 'qstring')
        return safe_key

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key not in self.key_storage:
            self.key_storage.append(self.__internalKeyCheck(key))
        self.store[key] = value

    def __delitem__(self, key):
        if key in self.key_storage:
            self.key_storage.remove(key)
        del self.store[key]

    def __iter__(self):
        return self.key_storage.__iter__()

    def __len__(self):
        return self.key_storage.__len__()
    
    def __str__(self):
        return self.store.__str__()
    
    def __contains__(self, item):
        return item in self.key_storage
    
    def __getattr__(self, attrib):
        return getattr(self.store, attrib)

    def __keytransform__(self, key):
        if isinstance(key, pbItem.pbItem):
            return key.value
        else:
            return key
    
    def sortedKeys(self):
        unsorted_keys = self.key_storage
        sorted_keys = sorted(unsorted_keys, cmp=KeySorter)
        can_sort = False
        if len(sorted_keys) > 0:
            all_dictionaries = all((type(self[key].value) is dict or type(self[key].value) is pbRoot) for key in unsorted_keys)
            if all_dictionaries:
                can_sort = all(self[key].get('isa', None) != None for key in unsorted_keys)
                if can_sort:
                    sorted_keys = sorted(unsorted_keys, key=lambda k: str(self[k]['isa']))
        return (can_sort, sorted_keys)
            