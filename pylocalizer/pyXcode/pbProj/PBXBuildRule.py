from .PBXItem import *

class PBXBuildRule(PBXItem):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)