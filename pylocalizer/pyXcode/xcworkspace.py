import os
import sys

# import the xcworkspacedata module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pyxcwsdata'))
from pyxcwsdata.xcworkspacedata import xcworkspacedata

# importing the xcscheme module
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pyxcscheme'))
from pyxcscheme import xcscheme

from Helpers import Logger

from xcodeproj import xcodeproj

class xcworkspace(object):
    
    def __init__(self, xcworkspace_file_path):
        if os.path.exists(xcworkspace_file_path):
            if xcworkspace_file_path.endswith('.xcworkspace'):
                self.filePath = xcworkspace_file_path
                
                # loading the pbxproj
                workspace_data_path = os.path.join(self.filePath, 'contents.xcworkspacedata')
                if os.path.exists(workspace_data_path):
                    self.contentsFile = xcworkspacedata(workspace_data_path)
                else:
                    Logger.write().error('Could not find the xcworkspacedata file!')
                
                # load schemes
                self.schemes = xcscheme.LoadSchemes(self.filePath)
                
            else:
                Logger.write().error('Not a Xcode workspace file!')
        else:
            Logger.write().error('Could not find the Xcode workspace file!')
    
    def projects(self):
        project_list = list()
        for project_file_path in self.contentsFile.projects():
            project_list.append(xcodeproj(project_file_path))
        return project_list
    
    def hasSchemeWithName(self, scheme_name):
        """
        This method is used for both 'xcworkspace' and 'xcodeproj' classes. It returns a two
        element tuple that contains the following:
        
        First element:
            A 'True' or 'False' value indicating if a scheme with the passed name was found in 
            this project or workspace file.
        
        Second element:
            The scheme object if a scheme with matching name was found, None otherwise.
        """
        found_scheme = None
        scheme_filter = filter(lambda scheme: scheme.name == scheme_name, self.schemes)
        if len(scheme_filter) > 0:
            found_scheme = scheme_filter[0]
        return (found_scheme != None, found_scheme)