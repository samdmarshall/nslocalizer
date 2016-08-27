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

from ..Helpers.Logger                           import Logger
from ..xcodeproj.pbProj                         import pbProj
from ..xcodeproj.pbProj.PBXSourcesBuildPhase    import PBXSourcesBuildPhase
from ..xcodeproj.pbProj.PBXVariantGroup         import PBXVariantGroup
from .                                          import PathFinder

def FilterByName(items, name) -> object:
    matched_items = [item for item in items if item.store[pbProj.PBX_Constants.kPBX_REFERENCE_name] == name]
    if len(matched_items):
        matched_items = matched_items[0]
    else:
        matched_items = None
    return matched_items

def getLocalizationFiles(project) -> (dict, dict):
    Logger.write().info('Filtering for Localizable.strings and Localizable.stringsdict files...')
    variant_groups = [pbx_object for pbx_object in project.pbx_objects if isinstance(pbx_object, PBXVariantGroup)]

    # localizable.strings
    localizable_strings = FilterByName(variant_groups, 'Localizable.strings')

    # localizable.stringsdict
    localizable_stringsdict = FilterByName(variant_groups, 'Localizable.stringsdict')

    Logger.write().info('Resolving language-specific file paths...')

    strings_file_refs = list()
    if localizable_strings is not None:
        languages = localizable_strings.store[pbProj.PBX_Constants.kPBX_REFERENCE_children]
        strings_file_refs = [PathFinder.resolveFilePathForReference(project, language_file) for language_file in languages]

    stringsdict_file_refs = list()
    if localizable_stringsdict is not None:
        language_dicts = localizable_stringsdict.store[pbProj.PBX_Constants.kPBX_REFERENCE_children]
        stringsdict_file_refs = [PathFinder.resolveFilePathForReference(project, language_file_dict) for language_file_dict in language_dicts]

    return (strings_file_refs, stringsdict_file_refs)
