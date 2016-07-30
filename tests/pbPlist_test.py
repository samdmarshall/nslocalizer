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
import unittest
from pylocalizer.xcodeproj.pbProj.pbPlist         import pbPlist
from pylocalizer.xcodeproj.pbProj.pbPlist.pbRoot  import pbRoot

test_directory_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pbPlist-test-data')

def readAndWritefile(test_directory):
    test_directory_path = os.path.join(test_directory_root, test_directory)

    test_path = os.path.join(test_directory_path, 'test.plist')
    output_path = os.path.join(test_directory_path, 'output.plist')
    
    test_input = pbPlist.PBPlist(test_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)

    return (test_input, test_output)

class pbPlistTestCases(unittest.TestCase):
    
    def test_array_encoding_hint(self):
        test_input, test_output = readAndWritefile('array_encoding_hint')
        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)
        self.assertNotEqual(len(str(test_input.root)), 0)
        self.assertNotEqual(len(str(test_output.root)), 0)
        self.assertEqual(len(str(test_input.root)), len(str(test_output.root)))

    def test_array_qstrings(self):
        test_input, test_output = readAndWritefile('array_qstrings')

        item_one = 'hello world!'
        item_two = 'this is a test'
        item_three = 'Of quoted strings'

        input_items = test_input.root
        self.assertEqual(input_items[0], item_one)
        self.assertEqual(input_items[1], item_two)
        self.assertEqual(input_items[2], item_three)

        output_items = test_output.root
        self.assertEqual(output_items[0], item_one)
        self.assertEqual(output_items[1], item_two)
        self.assertEqual(output_items[2], item_three)

        self.assertEqual(input_items[0], output_items[0])
        self.assertEqual(input_items[1], output_items[1])
        self.assertEqual(input_items[2], output_items[2])

        self.assertEqual(input_items, output_items)

    def test_array_strings(self):
        test_input, test_output = readAndWritefile('array_strings')

        item_one = 'obj1'
        item_two = 'obj2'
        item_three = 'obj3'
        
        input_items = test_input.root
        self.assertEqual(input_items[0], item_one)
        self.assertEqual(input_items[1], item_two)
        self.assertEqual(input_items[2], item_three)

        output_items = test_output.root
        self.assertEqual(output_items[0], item_one)
        self.assertEqual(output_items[1], item_two)
        self.assertEqual(output_items[2], item_three)

        self.assertEqual(input_items[0], output_items[0])
        self.assertEqual(input_items[1], output_items[1])
        self.assertEqual(input_items[2], output_items[2])

        self.assertEqual(input_items, output_items)

    def test_data_encoding_hint(self):
        test_input, test_output = readAndWritefile('data_encoding_hint')

        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)

        self.assertEqual(test_input.root, test_output.root)

    def test_dict_encoding_hint(self):
        test_input, test_output = readAndWritefile('dict_encoding_hint')

        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)

        self.assertTrue(isinstance(list(test_input.root.keys()), list))
        self.assertTrue(len(test_input.root.keys()) == 0)
        
        self.assertTrue(isinstance(list(test_output.root.keys()), list))
        self.assertTrue(len(test_output.root.keys()) == 0)

    def test_dict_string_values(self):
        test_input, test_output = readAndWritefile('dict_string_values')

        test_key_list = ['a', 'b', 'c', 'd']
        
        self.assertTrue(isinstance(list(test_input.root.keys()), list))
        self.assertTrue(len(test_input.root.keys()) == 4)
        self.assertEqual(set(test_input.root.keys()), set(test_key_list))

        self.assertTrue(isinstance(list(test_output.root.keys()), list))
        self.assertTrue(len(test_output.root.keys()) == 4)
        self.assertEqual(set(test_output.root.keys()), set(test_key_list))
        
        for key in test_input.root.keys():
            self.assertEqual(test_input.root[key], test_output.root[key])
        
        for key in test_output.root.keys():
            self.assertEqual(test_output.root[key], test_input.root[key])

    def test_empty_encoding_hint(self):
        test_input, test_output = readAndWritefile('empty_encoding_hint')

        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)

        self.assertIsNone(test_input.root)
        self.assertIsNone(test_output.root)
        self.assertEqual(test_input.root, test_output.root)

    def test_empty_plist(self):
        test_input, test_output = readAndWritefile('empty_plist')

        self.assertIsNone(test_input.string_encoding)
        self.assertIsNone(test_output.string_encoding)
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)

        self.assertIsNone(test_input.root)
        self.assertIsNone(test_output.root)
        self.assertEqual(test_input.root, test_output.root)

    def test_qstring_encoding_hint(self):
        test_input, test_output = readAndWritefile('qstring_encoding_hint')

        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)

        self.assertEqual(test_input.root, test_output.root)

    def test_raw_array(self):
        test_input, test_output = readAndWritefile('raw_array')

        self.assertTrue(isinstance(test_input.root.value, list))
        self.assertTrue(isinstance(test_output.root.value, list))

    def test_raw_data(self):
        test_input, test_output = readAndWritefile('raw_data')

        self.assertTrue(isinstance(test_input.root.value, bytearray))
        self.assertTrue(isinstance(test_output.root.value, bytearray))

    def test_raw_dict(self):
        test_input, test_output = readAndWritefile('raw_dict')

        self.assertTrue(isinstance(test_input.root.value, pbRoot))
        self.assertTrue(isinstance(test_output.root.value, pbRoot))

    def test_raw_qstring(self):
        test_input, test_output = readAndWritefile('raw_qstring')

        self.assertTrue(isinstance(test_input.root.value, str))
        self.assertTrue(isinstance(test_output.root.value, str))

    def test_raw_string(self):
        test_input, test_output = readAndWritefile('raw_string')

        self.assertTrue(isinstance(test_input.root.value, str))
        self.assertTrue(isinstance(test_output.root.value, str))

    def test_string_encoding_hint(self):
        test_input, test_output = readAndWritefile('string_encoding_hint')

        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)

        self.assertEqual(test_input.root, test_output.root)

    def test_xcode_proj(self):
        test_input, test_output = readAndWritefile('xcode_proj')

        self.assertEqual(test_input.string_encoding, 'UTF8')
        self.assertEqual(test_output.string_encoding, 'UTF8')
        self.assertEqual(test_input.string_encoding, test_output.string_encoding)
