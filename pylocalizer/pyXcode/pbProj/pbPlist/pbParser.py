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

from __future__    import print_function
import sys
from .             import StrParse
from .             import pbRoot
from .             import pbItem

class PBParser(object):

    def __init__(self, file_path=None):
        self.index = 0
        self.string_encoding = None
        self.file_path = file_path
        self.file_type = None
        try:
            file_descriptor = open(file_path, 'r')
            self.data = file_descriptor.read()
            file_descriptor.close()
        except IOError as exception:
            print('I/O error({0}): {1}'.format(exception.errno, exception.strerror))
        except:
            print('Unexpected error:'+str(sys.exc_info()[0]))
            raise

    def read(self):
        parsed_plist = None
        prefix = self.data[0:6]
        if prefix == 'bplist' or prefix == '<?xml ':
            if prefix == 'bplist':
                self.file_type = 'binary'
                if not sys.version_info >= (3, 4):
                    message = 'Attempting to load file "%s": binary plists are currently not supported!' % (self.file_path)
                    raise Exception(message)
            if prefix == '<?xml ':
                self.file_type = 'xml'
            import plistlib
            parsed_plist = plistlib.readPlist(self.file_path)
        else:
            self.file_type = 'ascii'
            # test for encoding hint
            if self.data[0:2] == '//':
                # this is to try to see if we can locate the desired string encoding of the file
                import re
                result = re.search('^// !\$\*(.+?)\*\$!', self.data) # pylint: disable=anomalous-backslash-in-string
                if result:
                    self.string_encoding = result.group(1)
            #now return the parse
            parsed_plist = self.__readTest(True)
        return parsed_plist

    def __readTest(self, requires_object=True):
        read_result = None
        # can we parse this?
        can_parse, self.index, _annotation = StrParse.IndexOfNextNonSpace(self.data, self.index)
        # we can ignore the annotation value here
        if not can_parse:
            if self.index != len(self.data):
                if requires_object is True:
                    message = 'Invalid plist file!'
                    raise Exception(message)
        else:
            read_result = self.__parse(requires_object)
        return read_result

    def __parse(self, requires_object=True):
        parsed_item = None
        starting_character = self.data[self.index]
        # TODO: replace with switch statement
        if starting_character == '{':
            # parse dictionary
            parsed_item = pbItem.pbItemResolver(self.__parseDict(), 'dictionary') # pylint: disable=redefined-variable-type
        elif starting_character == '(':
            # parse array
            parsed_item = pbItem.pbItemResolver(self.__parseArray(), 'array') # pylint: disable=redefined-variable-type
        elif starting_character == '<':
            # parse data
            parsed_item = pbItem.pbItemResolver(self.__parseData(), 'data') # pylint: disable=redefined-variable-type
        elif starting_character == '\'' or starting_character == '\"':
            # parse quoted string
            parsed_item = pbItem.pbItemResolver(self.__parseQuotedString(), 'qstring') # pylint: disable=redefined-variable-type
        elif StrParse.IsValidUnquotedStringCharacter(starting_character) is True:
            # parse unquoted string
            parsed_item = pbItem.pbItemResolver(self.__parseUnquotedString(), 'string') # pylint: disable=redefined-variable-type
        else:
            if requires_object is True:
                message = 'Unexpected character "0x'+str(format(ord(starting_character), 'x'))+'" at line '+str(StrParse.LineNumberForIndex(self.data, self.index))
                raise Exception(message)
        return parsed_item

    def __parseUnquotedString(self):
        string_length = len(self.data)
        start_index = self.index
        while self.index < string_length:
            current_char = self.data[self.index]
            if StrParse.IsValidUnquotedStringCharacter(current_char) is True:
                self.index += 1
            else:
                break
        if start_index != self.index:
            return self.data[start_index:self.index]
        else:
            message = 'Unexpected EOF'
            raise Exception(message)

    def __parseQuotedString(self):
        quote = self.data[self.index]
        string_length = len(self.data)
        self.index += 1 # skip over the first quote
        start_index = self.index
        while self.index < string_length:
            current_char = self.data[self.index]
            if current_char == quote:
                break
            if current_char == '\\':
                self.index += 2
            else:
                self.index += 1
        if self.index >= string_length:
            message = 'Unterminated quoted string starting on line '+str(StrParse.LineNumberForIndex(self.data, self.index))
            raise Exception(message)
        else:
            string_without_quotes = StrParse.UnQuotifyString(self.data, start_index, self.index)
            self.index += 1 # advance past quote character
            return string_without_quotes

    def __parseData(self):
        string_length = len(self.data)
        self.index += 1 # skip over "<"
        start_index = self.index
        end_index = 0
        byte_stream = ''
        while self.index < string_length:
            current_char = self.data[self.index]
            if current_char == '>':
                self.index += 1 # move past the ">"
                end_index = self.index
                break
            if StrParse.IsHexNumber(current_char) is True:
                byte_stream += current_char
            else:
                if not StrParse.IsDataFormattingWhitespace(current_char):
                    message = 'Malformed data byte group at line '+str(StrParse.LineNumberForIndex(self.data, self.index))+'; invalid hex'
                    raise Exception(message)
            self.index += 1
        if (len(byte_stream) % 2) == 1:
            message = 'Malformed data byte group at line '+str(StrParse.LineNumberForIndex(self.data, start_index))+'; uneven length'
            raise Exception(message)
        if end_index == 0:
            message = 'Expected terminating >" for data at line '+str(StrParse.LineNumberForIndex(self.data, start_index))
            raise Exception(message)
        data_object = bytearray.fromhex(byte_stream)
        return data_object

    def __parseArray(self):
        array_objects = list()
        self.index += 1  # move past the "("
        start_index = self.index
        new_object = self.__readTest(False)
        while new_object:
            can_parse, self.index, new_object.annotation = StrParse.IndexOfNextNonSpace(self.data, self.index)
            _can_parse = can_parse # pylint: disable=unused-variable
            array_objects.append(new_object)
            current_char = self.data[self.index]
            if current_char == ',':
                self.index += 1
            new_object = self.__readTest(False)
        current_char = self.data[self.index]
        if current_char != ')':
            message = 'Expected terminating ")" for array at line '+str(StrParse.LineNumberForIndex(self.data, start_index))
            raise Exception(message)
        self.index += 1 # skip over ending ")"
        return array_objects

    def __parseDict(self):
        dictionary = pbRoot.pbRoot()
        self.index += 1 # move past the "{"
        start_index = self.index
        new_object = self.__readTest(False)
        while new_object:
            can_parse, self.index, new_object.annotation = StrParse.IndexOfNextNonSpace(self.data, self.index)
            _can_parse = can_parse # pylint: disable=unused-variable
            key_object = new_object
            current_char = self.data[self.index]
            value_object = None
            if current_char == '=':
                self.index += 1
                value_object = self.__readTest(True)
            elif current_char == ';':
                # this is for strings files where the key and the value may be the same thing
                self.index += 1
                value_object = pbItem.pbItemResolver(new_object.value, new_object.type_name)
                value_object.annotation = new_object.annotation
            else:
                message = 'Missing ";" or "=" on line '+str(StrParse.LineNumberForIndex(self.data, self.index))
                raise Exception(message)
            can_parse, self.index, annotation = StrParse.IndexOfNextNonSpace(self.data, self.index)
            _can_parse = can_parse # pylint: disable=unused-variable
            if value_object.annotation is None: # this is to prevent losing the annotation of the key when parsing strings dicts
                value_object.annotation = annotation
            dictionary[key_object] = value_object
            current_char = self.data[self.index]
            if current_char == ';':
                self.index += 1 # advancing to the next key
            new_object = self.__readTest(False)
        current_char = self.data[self.index]
        if current_char != '}':
            message = 'Expected terminating "}" for dictionary at line '+str(StrParse.LineNumberForIndex(self.data, start_index))
            raise Exception(message)
        self.index += 1 # skip over ending "}"
        return dictionary
