import collections

from .PBX_Constants import *

class PBXItem(collections.MutableMapping):
    def __init__(self, identifier, dictionary):
        self.isa = dictionary.get(kPBX_isa, None)
        self.identifier = identifier
        self.store = dict()
        self.key_storage = set()
        self.update(dictionary)  # use the free update to set keys
        self.isResolved = False
    
    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        if key not in self.key_storage:
            self.key_storage.add(key)
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
        return self.__repr__()+'\n'+self.store.__str__()+'\n'
    
    def __contains__(self, item):
        return item in self.key_storage
    
    def __getattr__(self, attrib):
        return getattr(self.store, attrib)
    
    def __hash__(self):
        return hash(self.identifier)
    
    def __repr__(self):
        return '<%s : %s>' % (self.isa, self.identifier)
    
    def getGraphNodeWithIdentifier(self, identifier, project):
        found_object = project.objectForIdentifier(identifier)
        if found_object and found_object.isResolved == False:
            found_object.resolveGraph(project)
        return found_object
    
    def resolveGraphNodeForKey(self, key, project):
        identifier = self.get(key, None)
        if not isinstance(identifier, PBXItem):
            found_object = self.getGraphNodeWithIdentifier(identifier, project)
            if found_object:
                self[key] = found_object
    
    def resolveGraphNodesForArray(self, key, project):
        identifier_array = self.get(key, None)
        resolved_array = list()
        for identifier in identifier_array:
            resolved_item = self.getGraphNodeWithIdentifier(identifier, project)
            if resolved_item:
                resolved_array.append(resolved_item)
            else:
                resolved_array.append(identifier)
        self[key] = resolved_array
    
    def resolveGraph(self, project):
        self.isResolved = True

class PBX_Base_Target(PBXItem):
    def __init__(self, identifier, dictionary):
        super(PBX_Base_Target, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(PBX_Base_Target, self).resolveGraph(project)
        self.resolveGraphNodeForKey(kPBX_TARGET_buildConfigurationList, project)
        self.resolveGraphNodesForArray(kPBX_TARGET_buildPhases, project)
        self.resolveGraphNodesForArray(kPBX_TARGET_dependencies, project)
        self.resolveGraphNodeForKey(kPBX_TARGET_productReference, project)

class PBX_Base_Phase(PBXItem):
    def __init__(self, identifier, dictionary):
        super(PBX_Base_Phase, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(PBX_Base_Phase, self).resolveGraph(project)
        self.resolveGraphNodesForArray(kPBX_PHASE_files, project)

class PBX_Base_Reference(PBXItem):
    def __init__(self, identifier, dictionary):
        super(PBX_Base_Reference, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(PBX_Base_Reference, self).resolveGraph(project)
    def findParent(self, project):
        parent = None
        results = filter(lambda pbxref: isinstance(pbxref, PBX_Base_Reference) and kPBX_REFERENCE_children in pbxref.keys(), project.pbxObjects)
        for item in results:
            child_results = filter(lambda ref: self.identifier == ref.identifier, item[kPBX_REFERENCE_children])
            if len(child_results) > 0:
                parent = item
                break
        return parent