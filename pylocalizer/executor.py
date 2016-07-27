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

from __future__                                import print_function
import os
from .Helpers.Logger                        import Logger
from .xcodeproj.pbProj                        import pbProj
from .xcodeproj.pbProj.PBXSourcesBuildPhase    import PBXSourcesBuildPhase
from .xcodeproj.pbProj.PBXVariantGroup        import PBXVariantGroup

def getLocalizationFiles(project, target):
    variant_groups = [pbx_object for pbx_object in project.pbx_objects if isinstance(pbx_object, PBXVariantGroup)]

    # localizable.strings
    localizable_strings = [group for group in variant_groups if group.store[pbProj.PBX_Constants.kPBX_REFERENCE_name] == 'Localizable.strings']
    if len(localizable_strings):
        localizable_strings = localizable_strings[0]

#    # localizable.stringsdict
#    localizable_stringsdict = [group for group in variant_groups if group.store[pbProj.PBX_Constants.kPBX_REFERENCE_name] == 'Localizable.stringsdict']
#    if len(localizable_strings):
#        localizable_stringsdict = localizable_stringsdict[0]

    language_file_refs = list()
    languages = localizable_strings.store[pbProj.PBX_Constants.kPBX_REFERENCE_children]
    for language_file in languages:
        file_path = language_file.resolvePath(project)
        project_dir = os.path.dirname(os.path.dirname(project.pbx_file_path))
        file_path = os.path.join(project_dir, file_path)
        norm_file_path = os.path.normpath(file_path)
        language_file_refs.append(norm_file_path)

    return language_file_refs

def getCodeFileList(project, target):
    build_phases = target.store[pbProj.PBX_Constants.kPBX_TARGET_buildPhases]
    source_phases = [build_phase for build_phase in build_phases if isinstance(build_phase, PBXSourcesBuildPhase)]

    all_build_files = list()
    for phase in source_phases:
        all_build_files.extend(phase.store[pbProj.PBX_Constants.kPBX_PHASE_files])

    all_file_refs = list()
    for build_file in all_build_files:
        file_ref = build_file.store[pbProj.PBX_Constants.kPBX_BUILDFILE_fileRef]
        file_path = file_ref.resolvePath(project)
        project_dir = os.path.dirname(os.path.dirname(project.pbx_file_path))
        file_path = os.path.join(project_dir, file_path)
        norm_file_path = os.path.normpath(file_path)
        all_file_refs.append(norm_file_path)

    return all_file_refs

def findMissingStrings(project, target):
    code_files = getCodeFileList(project.project_file, target)
    localization_files = getLocalizationFiles(project.project_file, target)
    

def findUnusedStrings(project, target):
    code_files = getCodeFileList(project.project_file, target)
    localization_files = getLocalizationFiles(project.project_file, target)

