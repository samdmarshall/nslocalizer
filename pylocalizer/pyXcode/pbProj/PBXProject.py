from .PBXItem import *

class PBXProject_ProjectReference(PBXItem):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)
    def __repr__(self):
        return self.store.__repr__()
    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodeForKey(kPBX_PROJECTREF_ProjectRef, project)
        self.resolveGraphNodeForKey(kPBX_PROJECTREF_ProductGroup, project)

class PBXProject(PBXItem):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)
    def resolveGraph(self, project):
        super(self.__class__, self).resolveGraph(project)
        self.resolveGraphNodeForKey(kPBX_TARGET_buildConfigurationList, project)
        self.resolveGraphNodeForKey(kPBX_PROJECT_mainGroup, project)
        self.resolveGraphNodeForKey(kPBX_PROJECT_productRefGroup, project)
        self.resolveGraphNodesForArray(kPBX_PROJECT_targets, project)
        project_references = self.get(kPBX_PROJECT_projectReferences, None)
        if project_references:
            resolved_references = list()
            for reference in project_references:
                project_reference = PBXProject_ProjectReference(None, reference)
                project_reference.resolveGraph(project)
                resolved_references.append(project_reference)
            self[kPBX_PROJECT_projectReferences] = resolved_references