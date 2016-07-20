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