from Helpers import Logger
from Helpers import xcrun

# This is initial setup that should be done so the xcrun helper module doesn't have to be used everywhere.
import os
DEVELOPER_DIR = os.environ.get('DEVELOPER_DIR')
if DEVELOPER_DIR:
    Logger.write().info('DEVELOPER_DIR environment variable is already set, existing value "%s" will be used.' % (DEVELOPER_DIR))
else:
    os.environ['DEVELOPER_DIR'] = xcrun.resolve_developer_path()


import pyXcode
import xcodeproj
import xcworkspace