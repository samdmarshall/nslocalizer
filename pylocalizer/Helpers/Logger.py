# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/pyconfig
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

class Logger(object):
    __metaclass__ = Singleton
    _internal_logger = None

    def __init__(self, *args, **kwargs): # pragma: no cover
        pass

    @staticmethod
    def setupLogger():
        Logger._internal_logger = logging.getLogger('com.pewpewthespells.py.logging_helper')
        Logger._internal_logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('[%(levelname)s]: %(message)s')

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
