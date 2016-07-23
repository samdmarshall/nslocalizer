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

from .PBX_Constants import *

from .PBXItem import *

from .PBXAggregateTarget import *
from .PBXAppleScriptBuildPhase import *
from .PBXApplicationReference import *
from .PBXApplicationTarget import *
from .PBXBuildFile import *
from .PBXBuildRule import *
from .PBXBundleReference import *
from .PBXBundleTarget import *
from .PBXContainerItemProxy import *
from .PBXCopyFilesBuildPhase import *
from .PBXExecutableFileReference import *
from .PBXFileReference import *
from .PBXFrameworkReference import *
from .PBXFrameworksBuildPhase import *
from .PBXFrameworkTarget import *
from .PBXGroup import *
from .PBXHeadersBuildPhase import *
from .PBXJavaArchiveBuildPhase import *
from .PBXLegacyTarget import *
from .PBXLibraryReference import *
from .PBXLibraryTarget import *
from .PBXNativeTarget import *
from .PBXProject import *
from .PBXReferenceProxy import *
from .PBXResourcesBuildPhase import *
from .PBXRezBuildPhase import *
from .PBXShellScriptBuildPhase import *
from .PBXSourcesBuildPhase import *
from .PBXStandAloneTarget import *
from .PBXTargetDependency import *
from .PBXToolTarget import *
from .PBXVariantGroup import *
from .PBXZipArchiveReference import *
from .XCBuildConfiguration import *
from .XCConfigurationList import *

PBX_TYPE_TABLE = {
    'PBXAggregateTarget': PBXAggregateTarget,
    'PBXAppleScriptBuildPhase': PBXAppleScriptBuildPhase,
    'PBXApplicationReference': PBXApplicationReference,
    'PBXApplicationTarget': PBXApplicationTarget,
    'PBXBuildFile': PBXBuildFile,
    'PBXBuildRule': PBXBuildRule,
    'PBXBundleReference': PBXBundleReference,
    'PBXBundleTarget': PBXBundleTarget,
    'PBXContainerItemProxy': PBXContainerItemProxy,
    'PBXCopyFilesBuildPhase': PBXCopyFilesBuildPhase,
    'PBXExecutableFileReference': PBXExecutableFileReference,
    'PBXFileReference': PBXFileReference,
    'PBXFrameworkReference': PBXFrameworkReference,
    'PBXFrameworksBuildPhase': PBXFrameworksBuildPhase,
    'PBXFrameworkTarget': PBXFrameworkTarget,
    'PBXGroup': PBXGroup,
    'PBXHeadersBuildPhase': PBXHeadersBuildPhase,
    'PBXJavaArchiveBuildPhase': PBXJavaArchiveBuildPhase,
    'PBXLegacyTarget': PBXLegacyTarget,
    'PBXLibraryReference': PBXLibraryReference,
    'PBXLibraryTarget': PBXLibraryTarget,
    'PBXNativeTarget': PBXNativeTarget,
    'PBXProject': PBXProject,
    'PBXReferenceProxy': PBXReferenceProxy,
    'PBXResourcesBuildPhase': PBXResourcesBuildPhase,
    'PBXRezBuildPhase': PBXRezBuildPhase,
    'PBXShellScriptBuildPhase': PBXShellScriptBuildPhase,
    'PBXSourcesBuildPhase': PBXSourcesBuildPhase,
    'PBXStandAloneTarget': PBXStandAloneTarget,
    'PBXTargetDependency': PBXTargetDependency,
    'PBXToolTarget': PBXToolTarget,
    'PBXVariantGroup': PBXVariantGroup,
    'PBXZipArchiveReference': PBXZipArchiveReference,
    'XCBuildConfiguration': XCBuildConfiguration,
    'XCConfigurationList': XCConfigurationList,
}

def PBX_Type_Resolver(identifier, dictionary):
    global PBX_TYPE_TABLE
    object_type = dictionary.get(kPBX_isa, None)
    if object_type:
        return PBX_TYPE_TABLE.get(object_type, PBXItem)(identifier, dictionary)
    else:
        return None