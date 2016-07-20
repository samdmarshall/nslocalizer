import os

from .pbParser import PBParser
from .pbSerializer import PBSerializer

class PBPlist(object):
    
    def __init__(self, file_path):
        self.root = None
        if self.__checkFile(file_path) == True:
            parser = PBParser(self.file_path)
            self.root = parser.read()
            self.string_encoding = parser.string_encoding
            self.file_type = parser.file_type
    
    def write(self, file_path=None):
        if file_path == None:
            file_path = self.file_path
        serializer = PBSerializer(file_path, self.string_encoding, self.file_type)
        serializer.write(self.root)
    
    def __checkFile(self, file_path):
        can_access_file = os.path.exists(file_path)
        if can_access_file == True:
            self.file_path = file_path
        return can_access_file