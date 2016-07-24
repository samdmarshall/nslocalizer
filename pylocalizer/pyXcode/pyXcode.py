# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pylocalizer
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
from .                import xcodeproj
from .                import xcworkspace
from ..Helpers.Logger import Logger

class xcparse(object):

    def __init__(self, file_path):
        """
        Returns a xcparse object initialized from an xcodeproj or xcworkspace file.

        path should be the full path to a '.xcodeproj' or '.xcworkspace'.
        """
        if os.path.exists(file_path):
            self.file_path = os.path.abspath(file_path)
            self.name = os.path.basename(file_path)
            if self.name.endswith('.xcodeproj') or self.name.endswith('.pbproj'):
                project_file = xcodeproj.xcodeproj(self.file_path)
                self.root = project_file # pylint: disable=redefined-variable-type
            elif self.name.endswith('.xcworkspace'):
                workspace_file = xcworkspace.xcworkspace(self.file_path)
                self.root = workspace_file # pylint: disable=redefined-variable-type
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
        return self.name != '' and self.root != None

    def projects(self):
        """
        This method returns a list of 'xcodeproj' objects, one for each of the referenced
        project files in whatever root project or workspace was loaded. If there are
        multiple references to the same project file, this method will only one instance of that
        referenced project.
        """
        project_list = list()
        if self.isValid():
            project_list.append(self.root)
            project_list.extend(self._projects)
        return project_list
