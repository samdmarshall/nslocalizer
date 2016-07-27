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

from __future__           import print_function
import os
import sys
import argparse
from .version             import __version__ as PYLOCALIZER_VERSION
from .Helpers.Logger      import Logger
from .xcodeproj.xcodeproj import xcodeproj
from .                    import cache
from .                    import executor

# Main
def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='pylocalizer is a tool for identifying unused or missing localization string usage in Xcode projects')
    parser.add_argument(
        '--version',
        help='Displays the version information',
        action='version',
        version=PYLOCALIZER_VERSION
    )
    parser.add_argument(
        '--project',
        metavar='<Xcode project path>',
        help='specify the path to the .xcodeproj file',
        action='store'
    )
    parser.add_argument(
        '--target',
        metavar='<target name>',
        help='specify the name of the target to analyze',
        action='store'
    )
    parser.add_argument(
        '--find-missing',
        help='look for localized strings that are missing from any of the .strings files',
        action='store_true'
    )
    parser.add_argument(
        '--find-unused',
        help='look for localized strings that are not used in the code',
        action='store_true'
    )
    parser.add_argument(
        '--quiet',
        help='Silences all logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--verbose',
        help='Adds verbosity to logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--clean-cache',
        help='Clears the cache of all results',
        default=False,
        action='store_true'
    )

    args = parser.parse_args(argv)

    # perform the logging modifications before we do any other operations
    Logger.isVerbose(args.verbose)
    Logger.isSilent(args.quiet)

    if args.clean_cache:
        Logger.write().info('Cleaning all project caches...')

        # clean the cache
    else:
        has_set_flag = args.find_missing or args.find_unused
        can_run = args.project and args.target and has_set_flag

        if can_run:
            # parse project file
            project_file_path = os.path.normpath(args.project)
            xcodeproj_file = xcodeproj(project_file_path)

            # find target
            desired_target = [target for target in xcodeproj_file.project_file.targets() if target['name'] == args.target]
            if len(desired_target):
                desired_target = desired_target[0]
            else:
                desired_target = None

            if desired_target is not None:

                missing_strings = dict()
                unused_strings = dict()

                if args.find_missing:
                    missing_strings = executor.findMissingStrings(xcodeproj_file, desired_target)

                if args.find_unused:
                    unused_strings = executor.findUnusedStrings(xcodeproj_file, desired_target)

                # write data to persitance store

                # log data to xcode console

                # close up files
            else:
                Logger.write().info('Could not find target "%s" in the specified project file.')
        else:
            Logger.write().error('Please specify a project (--project) with a valid target (--target), and at least one search flag (--find-unused, --find-missing).')

if __name__ == "__main__": # pragma: no cover
    main()
