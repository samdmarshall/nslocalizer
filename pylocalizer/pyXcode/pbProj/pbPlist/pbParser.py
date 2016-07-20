import string_helper as StrParse
import pbRoot
import pbItem

class PBParser(object):
    
    def __init__(self, file_path=None):
        self.index = 0
        self.string_encoding = None
        self.file_path = file_path
        self.file_type = None
        try:
            fd = open(file_path, 'r')
            self.data = fd.read()
            fd.close()
        except IOError as e:
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))
        except:
            print('Unexpected error:'+str(sys.exc_info()[0]))
            raise
    
    def read(self):
        prefix = self.data[0:6]
        if prefix == 'bplist' or prefix == '<?xml ':
            if prefix == 'bplist':
                self.file_type = 'binary'
                import sys
                if not sys.version_info >= (3, 4):
                    message = 'Attempting to load file "%s": binary plists are currently not supported!' % (self.file_path)
                    raise Exception(message)
            if prefix == '<?xml ':
                self.file_type = 'xml'
            import plistlib
            return plistlib.readPlist(self.file_path)
        else:
            self.file_type = 'ascii'
            # test for encoding hint
            if self.data[0:2] == '//':
                # this is to try to see if we can locate the desired string encoding of the file
                import re
                result = re.search('^// !\$\*(.+?)\*\$!', self.data)
                if result:
                    self.string_encoding = result.group(1)
            #now return the parse
            return self.__readTest(True)
    
    def __readTest(self, requires_object=True):
        # can we parse this?
        can_parse, self.index, annotation = StrParse.IndexOfNextNonSpace(self.data, self.index) 
        # we can ignore the annotation value here
        if can_parse == False:
            if self.index != len(self.data):
                if requires_object == True:
                    message = 'Invalid plist file!'
                    raise Exception(message)
                return None
            else:
                return None
        else:
            return self.__parse(requires_object)
    
    def __parse(self, requires_object=True):
        starting_character = self.data[self.index]
        if starting_character == '{':
            # parse dictionary
            return pbItem.pbItemResolver(self.__parseDict(), 'dictionary')
        elif starting_character == '(':
            # parse array
            return pbItem.pbItemResolver(self.__parseArray(), 'array')
        elif starting_character == '<':
            # parse data
            return pbItem.pbItemResolver(self.__parseData(), 'data')
        elif starting_character == '\'' or starting_character == '\"':
            # parse quoted string
            return pbItem.pbItemResolver(self.__parseQuotedString(), 'qstring')
        elif StrParse.IsValidUnquotedStringCharacter(starting_character) == True:
            # parse unquoted string
            return pbItem.pbItemResolver(self.__parseUnquotedString(), 'string')
        else:
            if requires_object == True:
                message = 'Unexpected character "0x'+str(format(ord(starting_character), 'x'))+'" at line '+str(StrParse.LineNumberForIndex(self.data, self.index))
                raise Exception(message)
            else:
                return None
    
    def __parseUnquotedString(self):
        string_length = len(self.data)
        start_index = self.index
        while self.index < string_length:
            current_char = self.data[self.index]
            if StrParse.IsValidUnquotedStringCharacter(current_char) == True:
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
            if StrParse.IsHexNumber(current_char) == True:
                byte_stream += current_char
            else:
                if StrParse.IsDataFormattingWhitespace(current_char) == False:
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
        while new_object != None:
            can_parse, self.index, new_object.annotation = StrParse.IndexOfNextNonSpace(self.data, self.index)
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
        while new_object != None:
            can_parse, self.index, new_object.annotation = StrParse.IndexOfNextNonSpace(self.data, self.index)
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
            if value_object.annotation == None: # this is to prevent losing the annotation of the key when parsing strings dicts
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