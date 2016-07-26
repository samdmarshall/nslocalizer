import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    input_encoding_hint = 'UTF8'
    if not test_input.string_encoding == input_encoding_hint:
        print(u'\U0001F4A5 [INPUT] Expected encoding hint "%s", found "%s"' % (input_encoding_hint, test_input.string_encoding))
        raise Exception
    
    output_encoding_hint = 'UTF8'
    if not test_output.string_encoding == output_encoding_hint:
        print(u'\U0001F4A5 [OUTPUT] Expected encoding hint "%s", found "%s"' % (output_encoding_hint, test_output.string_encoding))
        raise Exception
    
    if not test_input.string_encoding == test_output.string_encoding:
        print(u'\U0001F4A5 [CMP] Mismatch encoding hints from INPUT "%s" and OUTPUT "%s"' % (test_input.string_encoding, test_output.string_encoding))
        raise Exception
    
    input_items = test_input.root
    if not input_items == None:
        print(u'\U0001F4A5 [] ')
        raise Exception
        
    output_items = test_output.root
    if not output_items == None:
        print(u'\U0001F4A5 [] ')
        raise Exception
        
    if not input_items == output_items:
        print(u'\U0001F4A5 [] ')
        raise Exception
        
except:
    raise