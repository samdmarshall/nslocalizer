#!/usr/bin/env python

import sys
import os
import filecmp
import shutil
import stat

# Copies the commit-msg file into the .git/hooks directory to be executed by
# git during commits if it does not already exist or if the file has been changed. 
# Files in the .git/hooks are not tracked, so any updates to commit-msg must 
# occur in the root and be copied over.
base_git_hooks_path = '.git/hooks/'
base_tools_hooks_path = './tools/hooks/'
hooks = [ 'pre-commit' ]

if not os.path.exists(base_git_hooks_path):
    os.mkdir(base_git_hooks_path)

for hook in hooks:
    tools_hook_path = os.path.join(base_tools_hooks_path, hook)
    git_hook_path = os.path.join(base_git_hooks_path, hook)
    shutil.copy2(tools_hook_path, git_hook_path)
    st = os.stat(git_hook_path)
    os.chmod(git_hook_path, st.st_mode | stat.S_IEXEC)
