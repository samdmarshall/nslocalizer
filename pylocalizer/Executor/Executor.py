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
from ..Helpers.Logger                           import Logger
from ..Language                                 import Language
from ..Language                                 import LanguageString
from ..Reporter                                 import Reporter
from ..Cache                                    import Cache
from ..xcodeproj.xcodeproj                      import xcodeproj
from ..Finder                                   import LanguageFinder
from ..Finder                                   import CodeFinder

class Executor(object):
    
    @classmethod
    def run(cls, arguments) -> None:
        has_set_flag = arguments.find_missing or arguments.find_unused
        can_run = arguments.project and arguments.target and has_set_flag

        xcodeproj_file = None
        desired_target = None

        if can_run:
            Logger.write().info('Loading project file...')
            # parse project file
            project_file_path = os.path.normpath(arguments.project)
            xcodeproj_file = xcodeproj(project_file_path)
            
            Logger.write().info('Search for target "%s" in project "%s"' % (arguments.target, os.path.basename(project_file_path)))
            # find target
            desired_target = [target for target in xcodeproj_file.project_file.targets() if target['name'] == arguments.target]
            if len(desired_target):
                desired_target = desired_target[0]
            else:
                desired_target = None
        else:
            Logger.write().error('Please specify a project (--project) with a valid target (--target), and at least one search flag (--find-unused, --find-missing).')

        if xcodeproj is not None and desired_target is not None:
                missing_strings = dict()
                unused_strings = dict()

                if arguments.find_missing:
                    missing_strings = findMissingStrings(xcodeproj_file, desired_target)
                    # log data to xcode console
                    Reporter.logWarnings(missing_strings, arguments.ignore)

                if arguments.find_unused:
                    unused_strings = findUnusedStrings(xcodeproj_file, desired_target)
                    # log data to xcode console
                    Reporter.logWarnings(unused_strings, arguments.ignore)

                # write data to persitance store
                Cache.writeToCache((missing_strings, unused_strings))

                # close up files
        else:
            Logger.write().info('Could not find target "%s" in the specified project file.' % arguments.target)

def generateLanguages(project) -> set:
    strings_files, stringsdict_files = LanguageFinder.getLocalizationFiles(project.project_file)

    languages = [Language.Language(path) for path in strings_files]
    [language.loadStringsDictFile(stringsdict_files) for language in languages]

    return set(languages)

def findMissingStrings(project, target) -> dict:
    Logger.write().info('Finding strings that are missing from language files...')
    languages = generateLanguages(project)

    additional_languages = set([language for language in languages if language.code != 'Base'])
    base_language = languages.difference(additional_languages).pop()

    missing_results = [string.processMapping(base_language, additional_languages) for string in base_language.strings]

    return dict(missing_results)

def findUnusedStrings(project, target) -> dict:
    Logger.write().info('Finding strings that are unused but are in language files...')
    code_files = CodeFinder.getCodeFileList(project.project_file, target)
    languages = generateLanguages(project)

    return dict()
