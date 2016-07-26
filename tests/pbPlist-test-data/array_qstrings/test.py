import os
import pbPlist

tests_path = os.path.join(TEST_DIRECTORY, 'test.plist')
output_path = os.path.join(TEST_DIRECTORY, 'output.plist')

try:
    test_input = pbPlist.PBPlist(tests_path)
    test_input.write(output_path)
    test_output = pbPlist.PBPlist(output_path)
    
    item_one = 'hello world!'
    item_two = 'this is a test'
    item_three = 'Of quoted strings'
    
    input_items = test_input.root
    if not input_items[0] == item_one:
        print(u'\U0001F4A5 [] ')
        raise Exception
    if not input_items[1] == item_two:
        print(u'\U0001F4A5 [] ')
        raise Exception
    if not input_items[2] == item_three:
        print(u'\U0001F4A5 [] ')
        raise Exception
        
    output_items = test_output.root
    if not output_items[0] == item_one:
        print(u'\U0001F4A5 [] ')
        raise Exception
    if not output_items[1] == item_two:
        print(u'\U0001F4A5 [] ')
        raise Exception
    if not output_items[2] == item_three:
        print(u'\U0001F4A5 [] ')
        raise Exception
    
    if not input_items[0] == output_items[0]:
        print(u'\U0001F4A5 [] ')
        raise Exception
    if not input_items[1] == output_items[1]:
        print(u'\U0001F4A5 [] ')
        raise Exception
    if not input_items[2] == output_items[2]:
        print(u'\U0001F4A5 [] ')
        raise Exception
    
    if not (input_items == output_items):
        print(u'\U0001F4A5 [] ')
        raise Exception
    
except:
    raise