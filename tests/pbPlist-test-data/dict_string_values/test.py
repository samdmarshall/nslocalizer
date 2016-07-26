import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    test_key_list = ['a', 'b', 'c', 'd']
    
    input_item = test_input.root
    if not type(input_item.keys()) == list:
        print(u'\U0001F4A5 [] ')
        raise Exception
    
    if not len(input_item.keys()) == 4:
        print(u'\U0001F4A5 [] ')
        raise Exception

    if not set(input_item.keys()) == set(test_key_list):
        print(u'\U0001F4A5 [] ')
        raise Exception
    
    output_item = test_output.root
    if not type(output_item.keys()) == list:
        print(u'\U0001F4A5 [] ')
        raise Exception
        
    if not len(output_item.keys()) == 4:
        print(u'\U0001F4A5 [] ')
        raise Exception
    
    if not set(output_item.keys()) == set(test_key_list):
        print(u'\U0001F4A5 [] ')
        raise Exception
    
    for key in input_item.keys():
        if not input_item[key] == output_item[key]:
            print(u'\U0001F4A5 [] ')
            raise Exception
    
    for key in output_item.keys():
        if not output_item[key] == input_item[key]:
            print(u'\U0001F4A5 [] ')
            raise Exception
except:
    raise