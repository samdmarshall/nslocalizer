# this dangerfile sets values that will be consumed by the global danger 
# file. The global dangerfile is run automatically after this repo-specific 
# file is run. The global dangerfile is located at: https://github.com/samdmarshall/danger

# set the number of lines that must be changed before this classifies as a 'Big PR'
@SDM_DANGER_BIG_PR_LINES = 75

# set the files to watch and warn about if there are changes made
@SDM_DANGER_BUILD_FILES = ['Makefile', 'Gemfile', 'Dangerfile', 'circle.yml', '.codeclimate.yml', 'tox.ini', 'pylintrc']

# set the files to watch and warn about if there are 
@SDM_DANGER_INSTALL_REQUIREMENTS_FILES = ['requirements.txt', 'setup.py']

# set the files to watch and fail if there are changes
@SDM_DANGER_IMMUTABLE_FILES = ['LICENSE', 'contributing.md', 'contributing/code-of-conduct.md']

# mark the paths that should be reported as part of the circle ci build artifacts
@SDM_DANGER_REPORT_CIRCLE_CI_ARTIFACTS = Array[
  {
    'message'=> 'html coverage report',
    'path'=> 'htmlcov/index.html'
  },
  {
    'message'=> 'linter report',
    'path'=> 'lint_output.txt'
  }
]
