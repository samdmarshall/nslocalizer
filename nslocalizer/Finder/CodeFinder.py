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

from ..Helpers.Logger                           import Logger
from ..xcodeproj.pbProj                         import pbProj
from ..xcodeproj.pbProj.PBXSourcesBuildPhase    import PBXSourcesBuildPhase
from .                                          import PathFinder

def getCodeFileList(project, target) -> list:
    Logger.write().info('Finding Code files for target "%s"...' % target[pbProj.PBX_Constants.kPBX_TARGET_name])
    build_phases = target.store[pbProj.PBX_Constants.kPBX_TARGET_buildPhases]
    source_phases = [build_phase for build_phase in build_phases if isinstance(build_phase, PBXSourcesBuildPhase)]

    all_build_files = list()
    for phase in source_phases:
        all_build_files.extend(phase.store[pbProj.PBX_Constants.kPBX_PHASE_files])

    all_file_refs = [PathFinder.resolveFilePathForReference(project, build_file.store[pbProj.PBX_Constants.kPBX_BUILDFILE_fileRef]) for build_file in all_build_files]

    return all_file_refs
