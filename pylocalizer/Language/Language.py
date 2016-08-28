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
import sys
import langcodes
from pbPlist               import pbPlist
from pbPlist               import pbParser
from .LanguageString       import LanguageString
from ..Helpers.Logger      import Logger

def GetLanguageCodeFromPath(path) -> str:
    dirname = os.path.dirname(path)
    basename = os.path.basename(dirname)
    locale, _ = os.path.splitext(basename)
    return locale

def FindLineIndex(data, string) -> int:
    line_index = 0
    if data is not None:
        position = data.find(str(string))
        line_index = data[:position].count('\n') + 1
    return line_index

class Language(object):
    def __init__(self, strings_file_path):
        self.code = GetLanguageCodeFromPath(strings_file_path)
        self.name = langcodes.LanguageData(language=self.code).language_name()
        self.strings_file = strings_file_path
        self.stringsdict_file = None
        self.stringsdict = None
        self.strings = self.loadStrings(self.strings_file)

    def getFileData(self) -> object:
        data = None
        try:
            encoding = pbParser.GetFileEncoding(self.strings_file)
            file_descriptor = pbParser.OpenFileWithEncoding(self.strings_file, encoding)
            data = file_descriptor.read()
            file_descriptor.close()
        except IOError as exception: # pragma: no cover
            print('I/O error({0}): {1}'.format(exception.errno, exception.strerror))
        except: # pragma: no cover
            print('Unexpected error:'+str(sys.exc_info()[0]))
            raise
        return data

    def loadStrings(self, file_path) -> list:
        strings_file_contents = pbPlist.PBPlist(self.strings_file)
        results = [LanguageString(localized_string_key, strings_file_contents.root[localized_string_key]) for localized_string_key in list(strings_file_contents.root.keys())]
        return results

    def findStrings(self) -> None:
        Logger.write().info('Resolving line numbers for the %s file...' % os.path.basename(self.strings_file))
        data = self.getFileData()
        for lstring in self.strings:
            lstring.line_number = FindLineIndex(data, lstring.string)

    def loadStringsDictFile(self, stringsdict_file_array) -> None:
        for stringsdict_file in stringsdict_file_array:
            dict_locale = GetLanguageCodeFromPath(stringsdict_file)
            if self.code == dict_locale:
                self.stringsdict_file = stringsdict_file
                break
        if self.stringsdict_file is not None:
            self.stringsdict = self.loadStrings(self.stringsdict_file)

    def __repr__(self): # pragma: no cover
        return '<%s : %s>' % (type(self).__name__, self.name)
