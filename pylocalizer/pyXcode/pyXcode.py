import os

from xcodeproj import xcodeproj
from xcworkspace import xcworkspace

from Helpers import Logger

class xcparse(object):
    
    def __init__(self, file_path):
        """
        Returns a xcparse object initialized from an xcodeproj or xcworkspace file.
        
        path should be the full path to a '.xcodeproj' or '.xcworkspace'.
        """
        if os.path.exists(file_path):
            self.filePath = os.path.abspath(file_path)
            self.name = os.path.basename(file_path)
            if self.name.endswith('.xcodeproj') or self.name.endswith('.pbproj'):
                project_file = xcodeproj(self.filePath)
                self.root = project_file
            elif self.name.endswith('.xcworkspace'):
                workspace_file = xcworkspace(self.filePath)
                self.root = workspace_file
            else:
                Logger.write().error('[xcparse]: Invalid file!')
                
            if self.root:
                self._projects = self.root.projects()
            else:
                Logger.write().error('[xcparse]: Could not get root file!')
        else:
            Logger.write().error('[xcparse]: Could not find file!')
    
    def isValid(self):
        """
        Returns a boolean value if the xcparse object was able to load a project or workspace file
        """
        return self.name != '' and self.root != None;
    
    def projects(self):
        """
        This method returns a list of 'xcodeproj' objects, one for each of the referenced
        project files in whatever root project or workspace was loaded. If there are 
        multiple references to the same project file, this method will only one instance of that
        referenced project.
        """
        project_list = list();
        if self.isValid():
            project_list.append(self.root);
            project_list.extend(self._projects);
        return project_list;
    
    def schemes(self):
        """
        This method returns a list of schemes contained by the root project or workspace,
        as well as all referenced projects and workspaces. 
        """
        project_schemes = list()
        if self.isValid():
            project_schemes.extend([scheme for project in self.projects() for scheme in project.schemes])
        return project_schemes
    
    def findSchemeWithName(self, scheme_name):
        """
        This method returns a list of schemes with matching names to the passed name. List 
        items are tuples with the following elements:
        
        First element:
            A 'True' or 'False' value that indicates if a scheme was found
        
        Second element:
            'xcscheme' object of the scheme with matching name
        
        Third element:
            The container object for the scheme, either 'xcodeproj' or 'xcworkspace'
        """
        if self.isValid():
            results = map(lambda project: project.hasSchemeWithName(scheme_name) + (project,), self.projects())
            results = filter(lambda result: result[0] == True, results)
            if len(results) > 0:
                return results
        return [(False, None, None)]