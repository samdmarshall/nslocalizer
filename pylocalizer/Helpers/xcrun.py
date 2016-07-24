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
import subprocess
import hashlib
#import tempfile
import struct
import CoreFoundation
from .Logger    import Logger

DEVELOPER_DIR = os.environ.get('DEVELOPER_DIR')
if DEVELOPER_DIR:
    Logger.write().info('DEVELOPER_DIR environment variable is already set, existing value "%s" will be used.' % (DEVELOPER_DIR))
else:
    os.environ['DEVELOPER_DIR'] = resolve_developer_path()

def hashStringForPath(path):
    """
    Returns the hash for a project's DerivedData location.

    path is the filesystem path to the .xcodeproj file.
    """
    hash_context = hashlib.md5()
    hash_context.update(path)
    md5_digest_hex = hash_context.digest()

    hash_path = [None] * 28

    first_value = struct.unpack('>Q', md5_digest_hex[:8])[0]

    counter = 13
    while counter >= 0:
        hash_path[counter] = chr((first_value % 26) + ord('a'))
        first_value = first_value / 26
        counter -= 1

    second_value = struct.unpack('>Q', md5_digest_hex[8:])[0]

    counter = 27
    while counter > 13:
        hash_path[counter] = chr((second_value % 26) + ord('a'))
        second_value = second_value / 26
        counter -= 1

    hash_path_string = ''.join(hash_path)

    return hash_path_string

def ResolveDerivedDataPath(project):
    default_dd_path = os.path.expanduser("~/Library/Developer/Xcode/DerivedData/")
    derived_data = CoreFoundation.CFPreferencesCopyAppValue('IDECustomDerivedDataLocation', 'com.apple.dt.Xcode') # pylint: disable=no-member
    if derived_data is None:
        derived_data = default_dd_path
    else:
        if derived_data[0] != '/':
            derived_data = os.path.join(project.path, derived_data)
    return derived_data

def ResolveBuildLocation(project, sym_root):
    build_dir_path = ''
    derived_data = ResolveDerivedDataPath(project)

    location_style = CoreFoundation.CFPreferencesCopyAppValue('IDEBuildLocationStyle', 'com.apple.dt.Xcode') # pylint: disable=no-member
    if location_style == 'Unique':
        xcodeproj_path = os.path.join(project.projectRoot.obj_path, project.name)
        unique_path = hashStringForPath(xcodeproj_path)
        # this is missing the configuration path.
        project_dir_name = os.path.splitext(project.name)[0]+'-'+unique_path+'/Build/Products/'
        build_dir_path = os.path.join(derived_data, project_dir_name)
    elif location_style == 'Shared':
        shared_path = CoreFoundation.CFPreferencesCopyAppValue('IDESharedBuildFolderName', 'com.apple.dt.Xcode') # pylint: disable=no-member
        build_dir_path = os.path.join(derived_data, shared_path)
    elif location_style == 'Custom':
        location_type = CoreFoundation.CFPreferencesCopyAppValue('IDECustomBuildLocationType', 'com.apple.dt.Xcode') # pylint: disable=no-member
        custom_path = CoreFoundation.CFPreferencesCopyAppValue('IDECustomBuildProductsPath', 'com.apple.dt.Xcode') # pylint: disable=no-member
        if location_type == 'RelativeToDerivedData':
            build_dir_path = os.path.join(derived_data, custom_path)
        elif location_type == 'RelativeToWorkspace':
            build_dir_path = os.path.join(project.path.base_path, custom_path)
        elif location_type == 'Absolute':
            build_dir_path = custom_path
    elif location_style == 'DeterminedByTargets':
        # this is missing the configuration path
        build_dir_path = os.path.join(project.projectRoot.obj_path, sym_root)
    return build_dir_path

def IntermediatesBuildLocation(project, target_name, config_name, sym_root):
    build_dir_path = ResolveBuildLocation(project, sym_root)
    project_name = project.name.split('.')[0]
    project_dir_path = os.path.join(build_dir_path, project_name+'.build')
    config_dir_path = os.path.join(project_dir_path, config_name)
    target_dir_path = os.path.join(config_dir_path, target_name+'.build')
    return target_dir_path

def ProductsBuildLocation(project, sym_root):
    """
    Returns the full path to the location of the build products.

    project is the project that the build product is in.

    sym_root is the value of $(SYMROOT) for the current configuration
    """
    # this needs to also take CONFIGURATION_DIR
    build_dir_path = ResolveBuildLocation(project, sym_root)
    return build_dir_path

def resolvePathFromLocation(location_string, path, base_path):
    path_string = ''
    path_type, item_path = location_string.split(':')
    if path_type == 'group':
        path = os.path.join(base_path, path)
        path_string = os.path.join(path, item_path)
    elif path_type == 'absolute':
        path_string = item_path
    elif path_type == 'developer':
        path_string = os.path.join(resolve_developer_path(), item_path)
    elif path_type == 'container':
        path_string = os.path.join(base_path, item_path)
    else:
        Logger.write().error('[xcrun]: Invalid item path name!')
        path_string = item_path
    return path_string

#def make_subprocess_session(action_list):
#    script = '#!/bin/sh \n'
#    for action in action_list:
#        script += action + ';\n'
#    script_file = tempfile.NamedTemporaryFile('wt')
#    script_file.write(script)
#    script_file.flush()
#    proc = subprocess.Popen(['/bin/bash', script_file.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#    stdout = proc.communicate(action)[0]
#    return stdout

def make_subprocess_call(call_args, shell_state=False):
    error = 0
    output = ''
    try:
        output = subprocess.check_output(call_args, shell=shell_state)
        error = 0
    except subprocess.CalledProcessError as exception:
        output = exception.output
        error = exception.returncode
    return (output, error)

def make_xcrun_with_args(args_tuple):
    xcrun_result = make_subprocess_call((('xcrun',) + args_tuple))
    if xcrun_result[1] != 0:
        Logger.write().error('[xcrun]: Error in exec!')
        sys.exit()
    xcrun_output = xcrun_result[0].rstrip('\n')
    return xcrun_output

def resolve_sdk_path(sdk_name):
    return make_xcrun_with_args(('--show-sdk-path', '--sdk', sdk_name))

def resolve_developer_path():
    xcrun_result = make_subprocess_call(('xcode-select', '-p'))
    if xcrun_result[1] != 0:
        Logger.write().error('[xcrun]: Please run Xcode first!')
        sys.exit()
    developer_path = xcrun_result[0].rstrip('\n')
    return developer_path
