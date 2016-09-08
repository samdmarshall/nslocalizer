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

import sys
import argparse
from .version             import __version__ as PYLOCALIZER_VERSION
from .Helpers.Logger      import Logger
from .Executor.Executor   import Executor

# Main
def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='nslocalizer is a tool for identifying unused or missing localization string usage in Xcode projects')
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
        required=True,
        action='store'
    )
    parser.add_argument(
        '--target',
        metavar='<target name>',
        help='specify the name of targets to analyze, this accepts multiple target names',
        type=str,
        default=list(),
        required=True,
        action='store',
        nargs='*'
    )
    parser.add_argument(
        '--find-missing',
        help='look for localized strings that are missing from any of the .strings files',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--find-unused',
        help='look for localized strings that are not used in the code',
        default=False,
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
        '--ignore',
        help='Specify languages to ignore (by code; eg: German = de).',
        type=str,
        default=list(),
        nargs='*'
    )
    parser.add_argument(
        '--no-ansi',
        help='Disables the ANSI color codes as part of the logger',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--error',
        help='Changes warnings to errors',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--debug',
        help=argparse.SUPPRESS,
        default=False,
        action='store_true'
    )
    args = parser.parse_args(argv)

    # perform the logging modifications before we do any other operations
    Logger.disableANSI(args.no_ansi)
    Logger.enableDebugLogger(args.debug)
    Logger.isVerbose(args.verbose)
    Logger.isSilent(args.quiet)

    ignored_locales = ', '.join(args.ignore)
    Logger.write().info('Ignoring languages: %s' % ignored_locales)

    Executor.run(args)

if __name__ == "__main__": # pragma: no cover
    main()
