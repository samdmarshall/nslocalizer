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

# Variables

# path to installation record that gets written when performing:
# - make build2
# - make build3

INSTALLED_FILES_RECORD := ./installed_files.txt

# names of the executables that are used as a part of this project

PYTHON2_CMD := python
PYTHON3_CMD := python3
TOX_CMD := tox
COVERAGE_CMD := coverage
DANGER_CMD := danger
GEM_CMD := gem
FIND_CMD := find
RM_CMD := rm
WHICH_CMD := which
XARGS_CMD := xargs
PRINTF_CMD := printf
TOUCH_CMD := touch
CP_CMD := cp
CAT_CMD := cat
PIP_CMD := pip
PIP3_CMD := pip3
CCTREPORTER_CMD := codeclimate-test-reporter
UNAME_CMD := uname
EXIT_CMD := exit
TPUT_CMD := tput
TR_CMD := tr
PYLINT_CMD := pylint
BREW_CMD := brew
PYENV_CMD := pyenv

TOX_PYENV := tox-pyenv
PYOBJC_CORE := pyobjc-core
PYOBJC_COCOA := pyobjc-framework-Cocoa

# invoke the specific executable command

PYTHON2 = $(shell command -v $(PYTHON2_CMD) 2> /dev/null)
PYTHON3 = $(shell command -v $(PYTHON3_CMD) 2> /dev/null)
TOX = $(shell command -v $(TOX_CMD) 2> /dev/null)
COVERAGE = $(shell command -v $(COVERAGE_CMD) 2> /dev/null)
DANGER = $(shell command -v $(DANGER_CMD) 2> /dev/null)
GEM = $(shell command -v $(GEM_CMD) 2> /dev/null)
FIND = $(shell command -v $(FIND_CMD) 2> /dev/null)
RM = $(shell command -v $(RM_CMD) 2> /dev/null)
WHICH = $(shell command -v $(WHICH_CMD) 2> /dev/null)
XARGS = $(shell command -v $(XARGS_CMD) 2> /dev/null)
PRINTF = $(shell command -v $(PRINTF_CMD) 2> /dev/null)
TOUCH = $(shell command -v $(TOUCH_CMD) 2> /dev/null)
CP = $(shell command -v $(CP_CMD) 2> /dev/null)
CAT = $(shell command -v $(CAT_CMD) 2> /dev/null)
PIP = $(shell command -v $(PIP_CMD) 2> /dev/null)
PIP3 = $(shell command -v $(PIP3_CMD) 2> /dev/null)
CCTREPORTER = $(shell command -v $(CCTREPORTER_CMD) 2> /dev/null)
UNAME = $(shell command -v $(UNAME_CMD) 2> /dev/null)
EXIT = $(shell command -v $(EXIT_CMD) 2> /dev/null)
TPUT = $(shell command -v $(TPUT_CMD) 2> /dev/null)
TR = $(shell command -v $(TR_CMD) 2> /dev/null)
PYLINT = $(shell command -v $(PYLINT_CMD) 2> /dev/null)
BREW = $(shell command -v $(BREW_CMD) 2> /dev/null)
PYENV = $(shell command -v $(PYENV_CMD) 2> /dev/null)

SYSTEM := $(shell $(UNAME) -s)
ifeq ($(SYSTEM),Darwin)
	USER_FLAG := --user
else
	USER_FLAG := 
endif

TERM_COLUMNS := `$(TPUT) cols`
DISPLAY_SEPARATOR := $(PRINTF) "%*.s\n" $(TERM_COLUMNS) " " | $(TR) ' ' '='

# Targets

# --- 

checkfor = @$(PRINTF) "Checking for $1..."; \
if [ -z `$(WHICH) $1` ]; then \
	$(PRINTF) " no\n"; \
	$(EXIT) 1;\
else \
	$(PRINTF) " yes\n"; \
fi

check:
	$(call checkfor,$(WHICH_CMD))
	$(call checkfor,$(CAT_CMD))
	$(call checkfor,$(CP_CMD))
	$(call checkfor,$(TPUT_CMD))
	$(call checkfor,$(TR_CMD))
	$(call checkfor,$(PRINTF_CMD))
	$(call checkfor,$(TOUCH_CMD))
	$(call checkfor,$(FIND_CMD))
	$(call checkfor,$(XARGS_CMD))
	$(call checkfor,$(RM_CMD))
	$(call checkfor,$(BREW_CMD))
	$(call checkfor,$(PYTHON2_CMD))
	$(call checkfor,$(PYTHON3_CMD))
	$(call checkfor,$(PIP_CMD))
	$(call checkfor,$(PIP3_CMD))
	$(call checkfor,$(TOX_CMD))
	$(call checkfor,$(COVERAGE_CMD))
	$(call checkfor,$(PYLINT_CMD))
	$(call checkfor,$(PYENV_CMD))
	$(call checkfor,$(GEM_CMD))
	$(call checkfor,$(DANGER_CMD))
	@$(DISPLAY_SEPARATOR)

# --- 

pipinstall = @$(PIP) install $1 $(USER_FLAG)
pipthreeinstall = @$(PIP3_CMD) install $1
geminstall = @$(GEM) install $1 $(USER_FLAG)
brewinstall = @$(BREW) install $1

install-deps:
	$(call brewinstall,$(PYENV_CMD))
	$(call checkfor,$(PYTHON2_CMD))
	$(call checkfor,$(PIP_CMD))
	$(call pipinstall,$(COVERAGE_CMD))
	$(call pipinstall,$(TOX_CMD))
	$(call pipinstall,$(TOX_PYENV))
	$(call pipinstall,$(CCTREPORTER_CMD))
	$(call pipinstall,$(PYLINT_CMD))
	$(call pipinstall,$(PYOBJC_CORE))
	$(call pipinstall,$(PYOBJC_COCOA))
	@$(DISPLAY_SEPARATOR)
	$(call brewinstall,$(PYTHON3_CMD))
	$(call checkfor,$(PIP3_CMD))
	$(call pipthreeinstall,$(COVERAGE_CMD))
	$(call pipthreeinstall,$(TOX_CMD))
	$(call pipthreeinstall,$(TOX_PYENV))
	$(call pipthreeinstall,$(CCTREPORTER_CMD))
	$(call pipthreeinstall,$(PYLINT_CMD))
	$(call pipthreeinstall,$(PYOBJC_CORE))
	$(call pipthreeinstall,$(PYOBJC_COCOA))
	@$(DISPLAY_SEPARATOR)
	$(call checkfor,$(GEM_CMD))
	$(call geminstall,$(DANGER_CMD))
	@$(DISPLAY_SEPARATOR)

# --- 

# this is for installing any tools that we don't already have

install-tools: check
	@$(PRINTF) "Installing git hooks..."
	@$(PYTHON2) ./tools/hooks-config.py
	@$(PRINTF) " done!\n"
	@$(DISPLAY_SEPARATOR)

# --- 

removeall = $(RM) -rRf
cleanlocation = @$(FIND) $1 $2 -print0 | $(XARGS) -0 $(removeall)

clean: check
	@$(PRINTF) "Removing existing installation... "
	@$(TOUCH) $(INSTALLED_FILES_RECORD)
	@$(CAT) $(INSTALLED_FILES_RECORD) | $(XARGS) $(removeall)
	@$(removeall) ./pylocalizer.egg-info
	@$(removeall) ./build
	@$(removeall) ./dist
	@$(removeall) ./.tox
	@$(removeall) .coverage
	@$(removeall) ./htmlcov
	@$(removeall) ./.eggs
	$(call cleanlocation, ., -name ".DS_Store")
	$(call cleanlocation, ., -name "*.pyc")
	$(call cleanlocation, ., -name "__pycache__" -type d)
	$(call cleanlocation, ./tests/pbPlist-test-data -name "output.plist")
	@$(PRINTF) "done!\n"
	@$(DISPLAY_SEPARATOR)
	
# --- 

build2: clean
	$(PYTHON2) ./setup.py install $(USER_FLAG) --record $(INSTALLED_FILES_RECORD)
	@$(DISPLAY_SEPARATOR)
	
# --- 

build3: clean
	$(PYTHON3) ./setup.py install --record $(INSTALLED_FILES_RECORD)
	@$(DISPLAY_SEPARATOR)

# --- 

test: clean
	$(TOX)
	@$(DISPLAY_SEPARATOR)

# --- 

upload_artifacts = @$(PRINTF) "Checking for path to upload artifacts..." ; \
if [ -d $1 ] ; then \
	$(PRINTF) "uploading.\n" ; \
	$(CP) -r ./htmlcov $1 ; \
	$(CP) lint_output.txt $1 ; \
else \
	$(PRINTF) "skipping.\n" ; \
fi

run_cctreporter = @$(PRINTF) "Checking CI branch to upload coverage results... " ; \
if [ "$(CIRCLE_BRANCH)" = "develop" ]; then \
	$(PRINTF) "OK.\n"; \
	$(CCTREPORTER) --token $(value CIRCLECI_CODECLIMATE_TOKEN) ; \
else \
	$(PRINTF) "skipping.\n"; \
fi

checktest = @$(PRINTF) "Checking that coverage data exists... " ; \
if [ -e ./.coverage ] ; then \
	$(PRINTF) "ok!\n" ; \
else \
	$(PRINTF) "not found!\n" ; \
	$(PRINTF) "Please run 'make test' before running 'make report'\n" ; \
	exit 1 ; \
fi \

report: check
	@$(call checktest)
	$(COVERAGE) report
	@$(DISPLAY_SEPARATOR)
	@$(PRINTF) "Generating html report... "
	@$(COVERAGE) html
	@$(PRINTF) "done!\n"
	@$(PRINTF) "Generated html report is located at: ./htmlcov/index.html\n"
ifdef CIRCLE_ARTIFACTS
	@$(DISPLAY_SEPARATOR)
	$(call upload_artifacts,$(CIRCLE_ARTIFACTS))
endif
	@$(DISPLAY_SEPARATOR)
	$(call run_cctreporter)
	@$(DISPLAY_SEPARATOR)

# --- 

danger: check
	@$(PRINTF) "Running danger "
ifdef CIRCLECI_DANGER_GITHUB_API_TOKEN
	@$(PRINTF) "(PR)... \n"
	@export DANGER_GITHUB_API_TOKEN=$(value CIRCLECI_DANGER_GITHUB_API_TOKEN)
	@$(DANGER) --verbose
else
	@$(PRINTF) "(local)... \n"
	@$(DANGER) local --verbose
endif
	@$(DISPLAY_SEPARATOR)
	
# --- 

ci: test lint report danger

# ---

lint: check
	@$(TOUCH) lint_output.txt
	@$(PRINTF) "Running linter... "
	@$(PYLINT) --rcfile=pylintrc ./pylocalizer > lint_output.txt || :
	@$(PRINTF) " done!\n"
	@$(PRINTF) "Generated linter report: lint_output.txt\n"
	@$(DISPLAY_SEPARATOR)

# ---

.PHONY: danger lint ci report test build3 build2 clean install-tools install-deps check