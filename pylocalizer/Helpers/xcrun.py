import os
import sys
import subprocess
from subprocess import CalledProcessError
import hashlib
import CoreFoundation
import tempfile
import struct

class xcrun(object):
    """
    This class exists to execute 'xcrun' tools.
    """
    
    @classmethod
    def hashStringForPath(cls, path):
        """
        Returns the hash for a project's DerivedData location.
        
        path is the filesystem path to the .xcodeproj file.
        """
        hash_context = hashlib.md5();
        hash_context.update(path);
        md5_digest_hex = hash_context.digest();
        
        hash_path = [None] * 28;
        
        first_value = struct.unpack('>Q', md5_digest_hex[:8])[0];
        
        counter = 13;
        while counter >= 0:
            hash_path[counter] = chr((first_value % 26) + ord('a'));
            first_value = first_value / 26;
            counter -= 1;
        
        second_value = struct.unpack('>Q', md5_digest_hex[8:])[0];
        
        counter = 27;
        while counter > 13:
            hash_path[counter] = chr((second_value % 26) + ord('a'));
            second_value = second_value / 26;
            counter -= 1;
        
        hash_path = ''.join(hash_path);
        
        return hash_path;
    
    @classmethod
    def ResolveDerivedDataPath(cls):
        default_dd_path = os.path.expanduser("~/Library/Developer/Xcode/DerivedData/");
        relative_dd_path = False;
        derived_data = CoreFoundation.CFPreferencesCopyAppValue('IDECustomDerivedDataLocation', 'com.apple.dt.Xcode');
        if derived_data == None:
            derived_data = default_dd_path;
        else:
            if derived_data[0] != '/':
                derived_data = os.path.join(project.path, derived_data);
        return derived_data;
    
    @classmethod
    def ResolveBuildLocation(cls, project, sym_root):
        build_dir_path = '';
        derived_data = cls.ResolveDerivedDataPath();
        
        location_style = CoreFoundation.CFPreferencesCopyAppValue('IDEBuildLocationStyle', 'com.apple.dt.Xcode');
        if location_style == 'Unique':
            xcodeproj_path = os.path.join(project.projectRoot.obj_path, project.name);
            unique_path = cls.hashStringForPath(xcodeproj_path);
            # this is missing the configuration path.
            project_dir_name = os.path.splitext(project.name)[0]+'-'+unique_path+'/Build/Products/';
            build_dir_path = os.path.join(derived_data, project_dir_name);
        elif location_style == 'Shared':
            shared_path = CoreFoundation.CFPreferencesCopyAppValue('IDESharedBuildFolderName', 'com.apple.dt.Xcode');
            build_dir_path = os.path.join(derived_data, shared_path);
        elif location_style == 'Custom':
            location_type = CoreFoundation.CFPreferencesCopyAppValue('IDECustomBuildLocationType', 'com.apple.dt.Xcode');
            custom_path = CoreFoundation.CFPreferencesCopyAppValue('IDECustomBuildProductsPath', 'com.apple.dt.Xcode');
            if location_type == 'RelativeToDerivedData':
                build_dir_path = os.path.join(derived_data, custom_path);
            elif location_type == 'RelativeToWorkspace':
                build_dir_path = os.path.join(project.path.base_path, custom_path);
            elif location_type == 'Absolute':
                build_dir_path = custom_path;
        elif location_style == 'DeterminedByTargets':
            # this is missing the configuration path
            build_dir_path = os.path.join(project.projectRoot.obj_path, sym_root);
        
        return build_dir_path;
    
    @classmethod
    def IntermediatesBuildLocation(cls, project, target_name, config_name, sym_root):
        build_dir_path = cls.ResolveBuildLocation(project, sym_root);
        project_name = project.name.split('.')[0];
        project_dir_path = os.path.join(build_dir_path, project_name+'.build');
        config_dir_path = os.path.join(project_dir_path, config_name);
        target_dir_path = os.path.join(config_dir_path, target_name+'.build');
        
        return target_dir_path;
    
    @classmethod
    def ProductsBuildLocation(cls, project, sym_root):
        """
        Returns the full path to the location of the build products.
        
        project is the project that the build product is in.
        
        sym_root is the value of $(SYMROOT) for the current configuration
        """
        # this needs to also take CONFIGURATION_DIR
        build_dir_path = cls.ResolveBuildLocation(project, sym_root);
        
        return build_dir_path;
    
    @classmethod
    def resolvePathFromLocation(cls, location_string, path, base_path):
        path_type, item_path = location_string.split(':');
        if path_type == 'group':
            path = os.path.join(base_path, path);
            return os.path.join(path, item_path);
        elif path_type == 'absolute':
            return item_path;
        elif path_type == 'developer':
            return os.path.join(resolve_developer_path(), item_path);
        elif path_type == 'container':
            return os.path.join(base_path, item_path);
        else:
            print('[xcrun]: Invalid item path name!');
            return item_path;
    
    @classmethod
    def make_subprocess_session(cls, action_list):
        script = '#!/bin/sh \n';
        for action in action_list:
            script += action + ';\n';
        script_file = tempfile.NamedTemporaryFile('wt')
        script_file.write(script)
        script_file.flush()
        proc = subprocess.Popen(['/bin/bash', script_file.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = proc.communicate(action)[0];
        return stdout;
    
    @classmethod
    def make_subprocess_call(cls, call_args, shell_state=False):
        error = 0;
        output = '';
        try:
            output = subprocess.check_output(call_args, shell=shell_state);
            error = 0;
        except CalledProcessError as e:
            output = e.output;
            error = e.returncode;
        return (output, error);
    
    @classmethod
    def make_xcrun_with_args(cls, args_tuple):
        xcrun_result = cls.make_subprocess_call((('xcrun',) + args_tuple));
        if xcrun_result[1] != 0:
            print('[xcrun]: Error in exec!');
            sys.exit();
        xcrun_output = xcrun_result[0].rstrip('\n');
        return xcrun_output;
    
    @classmethod
    def resolve_sdk_path(cls, sdk_name):
        return cls.make_xcrun_with_args(('--show-sdk-path', '--sdk', sdk_name));
    
    @classmethod
    def resolve_developer_path(cls):
        platform_path = '';
        xcrun_result = cls.make_subprocess_call(('xcode-select', '-p'));
        if xcrun_result[1] != 0:
            print('[xcrun]: Please run Xcode first!');
            sys.exit();
        developer_path = xcrun_result[0].rstrip('\n');
        return developer_path;
    
    @classmethod
    def perform_xcodebuild(cls, project, scheme_name, type, scheme_config_settings):
        build_command = 'xcodebuild -project "'+project.path.obj_path+'" -scheme "'+scheme_name+'" ';
        for item in scheme_config_settings:
            build_command+=str(item)+' ';
        build_command+=' '+type;
        result = cls.make_subprocess_call(build_command, True);
        print result[0];