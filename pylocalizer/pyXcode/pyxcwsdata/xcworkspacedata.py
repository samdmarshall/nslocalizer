import os
import xml.etree.ElementTree as xml

from xcworkspacenode import xcworkspacenode

class xcworkspacedata(object):
    
    def __init__(self, wsdata_file_path):
        self.filePath = wsdata_file_path
        contents = None
        try:
            contents = xml.parse(self.filePath)
        except:
            print('Unable to load contents.xcworkspacedata file!')
            raise
        
        workspace_base_path = os.path.dirname(os.path.dirname(self.filePath))
        self.objects = xcworkspacenode.parseNodesWithPath(contents.getroot(), workspace_base_path)
        
    def projects(self):
        project_file_paths = list()
        for item in self.objects:
            if item.isFile() and item.filePath.endswith(('.xcodeproj', '.pbproj')):
                project_file_paths.append(item.filePath)
        return project_file_paths
                