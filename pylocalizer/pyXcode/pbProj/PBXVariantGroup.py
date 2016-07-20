from .PBXItem import *

class PBXVariantGroup(PBX_Base_Reference):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodesForArray(kPBX_REFERENCE_children, project)