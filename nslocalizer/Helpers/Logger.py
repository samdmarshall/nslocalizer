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

import logging

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs): # pragma: no cover
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#These are the sequences need to get colored ouput
RESET_SEQ = '\033[0m'
BOLD_SEQ = '\033[1m'

COLORS = {
    'BLACK': '\033[1;30m',
    'RED': '\033[1;31m',
    'GREEN': '\033[1;32m',
    'YELLOW': '\033[1;33m',
    'BLUE': '\033[1;34m',
    'MAGENTA': '\033[1;35m',
    'CYAN': '\033[1;36m',
    'WHITE': '\033[1;37m'
}

LEVELS = {
    'WARNING': COLORS['YELLOW'],
    'INFO': COLORS['BLACK'],
    'DEBUG': COLORS['MAGENTA'],
    'CRITICAL': COLORS['BLUE'],
    'ERROR': COLORS['RED']
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record): # pragma: no cover
        levelname = record.levelname
        if self.use_color and levelname in LEVELS:
            levelname_color = LEVELS[levelname] + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

class Logger(object):
    __metaclass__ = Singleton
    _internal_logger = None
    _debug_logging = False
    _use_ansi_codes = False

    def __init__(self, *args, **kwargs): # pragma: no cover
        pass

    @staticmethod
    def enableDebugLogger(is_debug_logger=False):
        Logger._debug_logging = is_debug_logger

    @staticmethod
    def disableANSI(disable_ansi=False):
        Logger._use_ansi_codes = not disable_ansi

    @staticmethod
    def setupLogger():
        Logger._internal_logger = logging.getLogger('com.pewpewthespells.py.logging_helper')

        level = logging.DEBUG if Logger._debug_logging else logging.INFO
        Logger._internal_logger.setLevel(level)

        handler = logging.StreamHandler()
        handler.setLevel(level)

        # create formatter
        formatter = None
        if Logger._debug_logging is True: # pragma: no cover
            formatter = ColoredFormatter('[%(levelname)s][%(filename)s:%(lineno)s]: %(message)s', Logger._use_ansi_codes)
        else:
            formatter = ColoredFormatter('[%(levelname)s]: %(message)s', Logger._use_ansi_codes)

        # add formatter to ch
        handler.setFormatter(formatter)

        # add ch to logger
        Logger._internal_logger.addHandler(handler)

    @staticmethod
    def isVerbose(verbose_logging=False):
        if Logger._internal_logger is None: # pragma: no cover
            Logger.setupLogger()
        if not verbose_logging:
            Logger._internal_logger.setLevel(logging.WARNING)

    @staticmethod
    def isSilent(should_quiet=False):
        if Logger._internal_logger is None: # pragma: no cover
            Logger.setupLogger()
        if should_quiet:
            logging_filter = logging.Filter(name='com.pewpewthespells.py.logging_helper.shut_up')
            Logger._internal_logger.addFilter(logging_filter)

    @staticmethod
    def write():
        if Logger._internal_logger is None: # pragma: no cover
            Logger.setupLogger()
        return Logger._internal_logger
