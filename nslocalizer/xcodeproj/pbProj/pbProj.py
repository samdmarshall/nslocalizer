# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/nslocalizer
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

import pbPlist
from .                  import PBX_Constants
from .                  import PBX_Lookup

class PBXProj(object):

    def __init__(self, file_path):
        plist = pbPlist.pbPlist.PBPlist(file_path)
        contents = plist.root.nativeType()

        self.pbx_objects = set()
        self.pbx_identifier = None
        self.pbx_root_object = None
        self.pbx_object_version = 0
        self.pbx_archive_version = 0
        if contents is not None:
            # get the path that we read from
            self.pbx_file_path = plist.file_path

            # get the root object identifier
            self.pbx_identifier = contents.get(PBX_Constants.kPBX_rootObject, None)

            # get the archive version number
            archive_version = contents.get(PBX_Constants.kPBX_archiveVersion, None)
            if archive_version:
                self.pbx_archive_version = int(archive_version)

            # get the object version number
            object_version = contents.get(PBX_Constants.kPBX_objectVersion, None)
            if object_version:
                self.pbx_object_version = int(object_version)

            # get the classes
            self.pbx_classes = contents.get(PBX_Constants.kPBX_classes, None)

            # get all the objects
            objects_dict = contents.get(PBX_Constants.kPBX_objects, None)

            self.pbx_objects = [PBX_Lookup.PBX_Type_Resolver(entry, value) for entry, value in list(objects_dict.items())]

            self.pbx_root_object = self.objectForIdentifier(self.pbx_identifier)
            self.pbx_root_object.resolveGraph(self)

    def __repr__(self):
        rep_string = '<%s : INVALID OBJECT>' % (self.__class__.__name__)
        if self.isValid():
            rep_string = '<%s : %s : %s>' % (self.__class__.__name__, self.pbx_identifier, self.pbx_file_path)
        return rep_string

    def __attrs(self):
        return (self.pbx_identifier, self.pbx_file_path)

    def __eq__(self, other):
        return isinstance(other, PBXProj) and self.pbx_identifier == other.pbx_identifier and self.pbx_file_path == other.pbx_file_path

    def __hash__(self):
        return hash(self.__attrs())

    def isValid(self):
        return self.pbx_identifier is not None

    def objectForIdentifier(self, identifier):
        """
        Returns the parsed object from the project file for matching identifier, if no matching object is found it will return None.
        """
        result = None
        if self.isValid():
            filter_results = [pbx_object for pbx_object in self.pbx_objects if pbx_object.identifier == identifier]
            if len(filter_results):
                result = filter_results[0]
        return result

    def projects(self):
        """
        This method returns a set of 'xcodeproj' objects that represents any referenced
        xcodeproj files in this project.
        """
        subprojects = set()
        if self.isValid():
            subprojects = [path for path in self.__subproject_paths()]
        return subprojects

    def __subproject_paths(self):
        """
        This method is for returning a list of paths to referenced project files in this
        xcodeproj file.
        """
        paths = list()
        if self.isValid():
            project_references = self.pbx_root_object.get(PBX_Constants.kPBX_PROJECT_projectReferences, None)
            if project_references:
                paths = [project_dict[PBX_Constants.kPBX_PROJECTREF_ProjectRef] for project_dict in project_references]
        return paths

    def targets(self):
        """
        This method will return a list of build targets that are associated with this xcodeproj.
        """
        targets = list()
        if self.isValid():
            target_list = self.pbx_root_object.get(PBX_Constants.kPBX_PROJECT_targets, None)
            if target_list:
                targets.extend(target_list)
        return targets
