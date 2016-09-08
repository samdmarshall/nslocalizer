# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/nslocalizer
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

def log(file_name, line_number, type_string, message_string) -> None:
    message = '%s:%s: %s: %s' % (file_name, line_number, type_string, message_string)
    ascii_message = message.encode('ascii', 'replace')
    display_message = ascii_message.decode('ascii', 'ignore')
    print(display_message)

def logError(file_name, line_number, message_string) -> None:
    log(file_name, line_number, 'error', message_string)

def logWarning(file_name, line_number, message_string) -> None:
    log(file_name, line_number, 'warning', message_string)

def logMissingStrings(warnings_dictionary, ignore_languages, is_error=False) -> None:
    keys = list(warnings_dictionary.keys())
    keys.sort(key=lambda string: string.line_number)
    for key in keys:
        locale_names = [language.name for language in warnings_dictionary.get(key) if language.code not in ignore_languages]
        if len(locale_names):
            message = ', '.join(locale_names)
            message_string = 'String "%s" missing for: %s' %  (key.string, message)
            if is_error is False:
                logWarning(key.base.strings_file, key.line_number, message_string)
            else:
                logError(key.base.strings_file, key.line_number, message_string)

def logUnusedStrings(unused_strings_list, is_error=False) -> None:
    unused_strings_list.sort(key=lambda string: string.line_number)
    for unused_string in unused_strings_list:
        message = 'String "%s" is not used' % unused_string.string
        if is_error is False:
            logWarning(unused_string.base.strings_file, unused_string.line_number, message)
        else:
            logError(unused_string.base.strings_file, unused_string.line_number, message)
