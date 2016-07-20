from .PBXItem import *

class PBXReferenceProxy(PBXItem):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodeForKey(kPBX_PROXY_remoteRef, project)