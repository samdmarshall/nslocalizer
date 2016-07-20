from .PBXItem import *

class PBXCopyFilesBuildPhase(PBX_Base_Phase):
    def __init__(self, identifier, dictionary):
        super(self.__class__, self).__init__(identifier, dictionary)