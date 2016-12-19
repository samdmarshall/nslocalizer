# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/nslocalizer
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

from . import PBX_Constants
from . import PBXItem
from . import PBXAggregateTarget
from . import PBXAppleScriptBuildPhase
from . import PBXApplicationReference
from . import PBXApplicationTarget
from . import PBXBuildFile
from . import PBXBuildRule
from . import PBXBundleReference
from . import PBXBundleTarget
from . import PBXContainerItemProxy
from . import PBXCopyFilesBuildPhase
from . import PBXExecutableFileReference
from . import PBXFileReference
from . import PBXFrameworkReference
from . import PBXFrameworksBuildPhase
from . import PBXFrameworkTarget
from . import PBXGroup
from . import PBXHeadersBuildPhase
from . import PBXJavaArchiveBuildPhase
from . import PBXLegacyTarget
from . import PBXLibraryReference
from . import PBXLibraryTarget
from . import PBXNativeTarget
from . import PBXProject
from . import PBXReferenceProxy
from . import PBXResourcesBuildPhase
from . import PBXRezBuildPhase
from . import PBXShellScriptBuildPhase
from . import PBXSourcesBuildPhase
from . import PBXStandAloneTarget
from . import PBXTargetDependency
from . import PBXToolTarget
from . import PBXVariantGroup
from . import PBXZipArchiveReference
from . import XCBuildConfiguration
from . import XCConfigurationList
from . import XCVersionGroup

PBX_TYPE_TABLE = {
    'PBXAggregateTarget': PBXAggregateTarget.PBXAggregateTarget,
    'PBXAppleScriptBuildPhase': PBXAppleScriptBuildPhase.PBXAppleScriptBuildPhase,
    'PBXApplicationReference': PBXApplicationReference.PBXApplicationReference,
    'PBXApplicationTarget': PBXApplicationTarget.PBXApplicationTarget,
    'PBXBuildFile': PBXBuildFile.PBXBuildFile,
    'PBXBuildRule': PBXBuildRule.PBXBuildRule,
    'PBXBundleReference': PBXBundleReference.PBXBundleReference,
    'PBXBundleTarget': PBXBundleTarget.PBXBundleTarget,
    'PBXContainerItemProxy': PBXContainerItemProxy.PBXContainerItemProxy,
    'PBXCopyFilesBuildPhase': PBXCopyFilesBuildPhase.PBXCopyFilesBuildPhase,
    'PBXExecutableFileReference': PBXExecutableFileReference.PBXExecutableFileReference,
    'PBXFileReference': PBXFileReference.PBXFileReference,
    'PBXFrameworkReference': PBXFrameworkReference.PBXFrameworkReference,
    'PBXFrameworksBuildPhase': PBXFrameworksBuildPhase.PBXFrameworksBuildPhase,
    'PBXFrameworkTarget': PBXFrameworkTarget.PBXFrameworkTarget,
    'PBXGroup': PBXGroup.PBXGroup,
    'PBXHeadersBuildPhase': PBXHeadersBuildPhase.PBXHeadersBuildPhase,
    'PBXJavaArchiveBuildPhase': PBXJavaArchiveBuildPhase.PBXJavaArchiveBuildPhase,
    'PBXLegacyTarget': PBXLegacyTarget.PBXLegacyTarget,
    'PBXLibraryReference': PBXLibraryReference.PBXLibraryReference,
    'PBXLibraryTarget': PBXLibraryTarget.PBXLibraryTarget,
    'PBXNativeTarget': PBXNativeTarget.PBXNativeTarget,
    'PBXProject': PBXProject.PBXProject,
    'PBXReferenceProxy': PBXReferenceProxy.PBXReferenceProxy,
    'PBXResourcesBuildPhase': PBXResourcesBuildPhase.PBXResourcesBuildPhase,
    'PBXRezBuildPhase': PBXRezBuildPhase.PBXRezBuildPhase,
    'PBXShellScriptBuildPhase': PBXShellScriptBuildPhase.PBXShellScriptBuildPhase,
    'PBXSourcesBuildPhase': PBXSourcesBuildPhase.PBXSourcesBuildPhase,
    'PBXStandAloneTarget': PBXStandAloneTarget.PBXStandAloneTarget,
    'PBXTargetDependency': PBXTargetDependency.PBXTargetDependency,
    'PBXToolTarget': PBXToolTarget.PBXToolTarget,
    'PBXVariantGroup': PBXVariantGroup.PBXVariantGroup,
    'PBXZipArchiveReference': PBXZipArchiveReference.PBXZipArchiveReference,
    'XCBuildConfiguration': XCBuildConfiguration.XCBuildConfiguration,
    'XCConfigurationList': XCConfigurationList.XCConfigurationList,
    'XCVersionGroup': XCVersionGroup.XCVersionGroup,
}

def PBX_Type_Resolver(identifier, dictionary):
    object_type = dictionary.get(PBX_Constants.kPBX_isa, None)
    result = None
    if object_type:
        result = PBX_TYPE_TABLE.get(object_type, PBXItem.PBXItem)(identifier, dictionary)
    return result
