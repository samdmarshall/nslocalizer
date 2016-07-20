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