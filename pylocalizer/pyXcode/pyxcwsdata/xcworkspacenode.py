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
import xml.etree.ElementTree as xml

class xcworkspacenode(object):
    def __init__(self, node, item_path):
        self.filePath = item_path
        self.children = None
        self.node = node
        if self.node.tag == 'Group':
            self.children = self.parseNodesWithPath(self.node, self.filePath)
    
    def isFile(self):
        return (self.node.tag == 'FileRef')
    
    def __repr__(self):
        children_string = ''
        if self.children != None:
            children_string = ' : %i children' % len(self.children)
        return '<%s : "%s"%s>' % (self.node.tag, self.filePath, children_string)
    
    @classmethod
    def resolvePathFromLocation(cls, location_string, path, base_path):
        path_type, item_path = location_string.split(':');
        if path_type == 'group':
            path = os.path.join(base_path, path);
            return os.path.join(path, item_path);
        elif path_type == 'absolute':
            return item_path;
        elif path_type == 'developer':
            developer_dir_path = os.environ.get('DEVELOPER_DIR', None)
            if not developer_dir_path:
                print('The environment variable "DEVELOPER_DIR" is not defined!')
                raise Exception
            return os.path.join(developer_dir_path, item_path);
        elif path_type == 'container':
            return os.path.join(base_path, item_path);
        else:
            print('Invalid item path name!');
            raise Exception
    
    @classmethod
    def resolvePathFromXMLNode(cls, node, item_path):
        file_relative_path = node.attrib['location']
        return cls.resolvePathFromLocation(file_relative_path, '', item_path)
    
    @classmethod
    def parseNodesWithPath(cls, nodes, starting_path):
        objects = list()
        for child in nodes:
            item_path = cls.resolvePathFromXMLNode(child, starting_path)
            child_object = None
            if child.tag == 'FileRef':
                child_object = cls(child, item_path)
            if child.tag == 'Group':
                child_object = cls(child, item_path)
            
            if child_object:
                objects.append(child_object)
        return objects