import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    input_item = test_input.root
    output_item = test_output.root
    
    if not type(input_item.value) == list:
        print(u'\U0001F4A5 [INPUT] Expected type "list", found "%s"' % (type(input_item.value)))
        raise Exception
        
    if not type(output_item.value) == list:
        print(u'\U0001F4A5 [OUTPUT] Expected type "list", found "%s"' % (type(output_item.value)))
        raise Exception
    
    if not type(input_item.value) == type(output_item.value):
        print(u'\U0001F4A5 [CMP] Mismatch type from INPUT "%s" and OUTPUT "%s"' % (type(input_item.value), type(output_item.value)))
        raise Exception
except:
    raise