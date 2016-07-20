import sys

class PBSerializer(object):
    
    def __init__(self, file_path=None, encoding=None, file_type=None):
        self.string_encoding = encoding
        self.file_path = file_path
        self.file_type = file_type
    
    def write(self, obj=None):
        if self.file_type == 'ascii':
            try:
                fd = open(self.file_path, 'w')
                self.__writeObject(fd, obj)
                fd.close()
            except IOError as e:
                print('I/O error({0}): {1}'.format(e.errno, e.strerror))
            except:
                print('Unexpected error:'+str(sys.exc_info()[0]))
                raise
        else:
            import plistlib
            plistlib.writePlist(obj, self.file_path)
    
    def __writeObject(self, fd=None, obj=None):
        if fd == None:
            message = 'Fatal error, file descriptor is None'
            raise TypeError(message)
        if self.string_encoding != None:
            fd.write('// !$*'+self.string_encoding+'*$!\n')
        if obj != None:
            write_string, indent_level = obj.writeString()
            fd.write(write_string)